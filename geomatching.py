import gspread
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint
import time
from math import radians, cos, sin, asin, sqrt 

def main():
    return setupGspread()

def setupGspread():
    scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("/Users/ruchirbaronia/PycharmProjects/CoronaVirus/OaklandAtRisk Project/oaklandAtRiskFlaskApp/credentials.json", scope)
    client = gspread.authorize(creds)

    request_sheet = client.open("oakland_at_risk_database_testing").worksheet("RequestQuery")  # Open the spreadsheet
    request_data = request_sheet.get_all_records()  # Get a list of all records


    volunteer_sheet = client.open("oakland_at_risk_database_testing").worksheet("VolunteerQuery")
    volunteer_data = volunteer_sheet.get_all_records()
    

    return formatData(request_data, volunteer_data)

def formatData(request_data, volunteer_data):
    
    volunteer_dict = {}
    for elem in volunteer_data:
        volunteer_dict[elem['TIMESTAMP']] = {key:val for key,val in elem.items() if key != 'TIMESTAMP' and key != 'DATE' and key != 'TIME' and key != 'EXTRA' and key != 'INFO' and key != 'EXTRA1'}

    request_dict = {}
    for elem in request_data:
        request_dict[elem['TIMESTAMP']] = {key:val for key,val in elem.items() if key != 'TIMESTAMP' and key != 'DATE' and key != 'TIME' and key != 'EXTRA' and key != 'EXTRA1' and key != 'EXTRA2' and key!= 'EXTRA3' and key != 'EXTRA4'}

    print(request_dict)
    return volunteer_dict, request_dict

def find_eight_closest(timestamp, volunteer_dict, request_dict, language = None):
    if request_dict[timestamp]['LANGUAGE'] == '' or 'nglish' in request_dict[timestamp]['LANGUAGE']:
        language = None
    else:
        language = request_dict[timestamp]['LANGUAGE']

    def distance(lat1, lat2, lon1, lon2):
        lon1 = radians(lon1)
        lon2 = radians(lon2)
        lat1 = radians(lat1)
        lat2 = radians(lat2)
        # Haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * asin(sqrt(a))
        r = 3956
        # calculate the result
        return(c * r)
    
    eight_closest = []
    
    request_lat = float(request_dict[timestamp]['LOC'].split(',')[0])
    request_lon = float(request_dict[timestamp]['LOC'].split(',')[1])

    for elem in volunteer_dict.keys():
        if language == None:
            if volunteer_dict[elem]['LOC']:
                if eight_closest == [] or len(eight_closest) < 8:
                    eight_closest.append((distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])), elem))
                elif max([tup0[0] for tup0 in eight_closest]) > distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])): 
                    max_dist = max([tup0[0] for tup0 in eight_closest])
                    max_timestamp = ''
                    for maxcan in eight_closest:
                        if maxcan[0] == max_dist:
                            max_timestamp = maxcan[1]
                    eight_closest.remove((max_dist, max_timestamp))
                    eight_closest.append((distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])), elem))
        elif volunteer_dict[elem]['LANGUAGE'] and language[1:] in volunteer_dict[elem]['LANGUAGE']:
            if volunteer_dict[elem]['LOC']:
                if eight_closest == [] or len(eight_closest) < 8:
                    eight_closest.append((distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])), elem))
                elif max([tup0[0] for tup0 in eight_closest]) > distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])):
                    max_dist = max([tup0[0] for tup0 in eight_closest])
                    max_timestamp = ''
                    for maxcan in eight_closest:
                        if maxcan[0] == max_dist:
                            max_timestamp = maxcan[1]
                    eight_closest.remove((max_dist, max_timestamp))
                    eight_closest.append((distance(request_lat, float(volunteer_dict[elem]['LOC'].split(',')[0]), request_lon, float(volunteer_dict[elem]['LOC'].split(',')[1])), elem))


    
    request_info_dict = {key:val for key,val in request_dict[timestamp].items() if key != 'LOC'}
    match_infos = []
    for timeval in eight_closest:
        match_infos.append({key:val for key,val in volunteer_dict[timeval[1]].items() if key != 'LOC'})

    return request_info_dict, match_infos

if __name__ == '__main__':
    pprint(find_eight_closest(43973.59278, main()[0], main()[1]))
