from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager
import geomatching
import date_to_string

app = Flask(__name__)


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
    volunteer_dict, request_dict = geomatching.main()
    newDict = {key: value for key, value in request_dict.items() if key > date}
    return newDict

@app.route('/1', methods=["GET"])
def functest():
    ids = request.args.getlist('ids')
    info = []
    volunteer_dict, request_dict = geomatching.main()
    for elem in ids:
        info.append((elem, eightclosestinfo(elem, volunteer_dict, request_dict)))
    return render_template('afterchoosing.html', ids1=info)

def eightclosestinfo(name, volunteer_dict, request_dict):
    for elem in request_dict:
        if name in request_dict[elem]['NAME']:
            return geomatching.find_eight_closest(elem, volunteer_dict, request_dict)[1]

if __name__ == '__main__':
    app.run()

