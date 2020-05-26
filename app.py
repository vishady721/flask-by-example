from flask import Flask, render_template, jsonify, request
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
    nameList = [dict["NAME"] for dict in relevantRequesters.values()]
    print(nameList)
    return render_template('requestersChecklist.html', ids= nameList)


def getRequestersAfterDate(date):
    volunteer_dict, request_dict = geomatching.main()
    newDict = {key: value for key, value in volunteer_dict.items() if key > date}
    return newDict

@app.route('/1', methods=["GET"])
def functest():
    ids = [elem for elem in request.args.get("ids")]
    return render_template('afterchoosing.html', ids1=ids)

if __name__ == '__main__':
    app.run()

