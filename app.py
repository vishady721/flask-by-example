from flask import Flask, render_template, jsonify, request
import geomatching
import date_to_string

app = Flask(__name__)
volunteer_dict, request_dict = geomatching.main()

@app.route('/')
def main():
    return render_template('dateChooser.html')

@app.route('/', methods=["POST"])
def postMethod():
    dateString = request.form["date"]
    relevantRequesters = getRequestersAfterDate(date_to_string.date_to_num(dateString))
    print("Date to Number {}".format(date_to_string.date_to_num(dateString)))
    print("Relevant Requesters" +str(relevantRequesters))
    nameList = [dict_["NAME"] for dict_ in relevantRequesters.values()]
    print(nameList)
    return render_template('requestersChecklist.html', ids= nameList)


def getRequestersAfterDate(date):
    newDict = {key: value for key, value in volunteer_dict.items() if key > date}
    return newDict

@app.route('/1', methods=["GET"])
def functest():
    ids = request.args.getlist('ids')
    info = []
    for elem in ids:
        info.append(eightclosestinfo(elem, volunteer_dict, request_dict))
    return render_template('afterchoosing.html', ids1=info)

def eightclosestinfo(name, volunteer_dict, request_dict):
    for elem in request_dict:
        if request_dict[elem]['NAME'] == name:
            return geomatching.find_eight_closest(elem, volunteer_dict, request_dict)

if __name__ == '__main__':
    app.run()

