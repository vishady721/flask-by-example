from flask import Flask, render_template, jsonify, request
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user
import geomatching
import date_to_string

app = Flask(__name__)
# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login" #Whenever the user needs to login, it will look for the app.route with /login

# config
app.config.update(
    DEBUG = True,
    SECRET_KEY = 'secret_xxx'
)

@app.route('/')
@login_required
def main():
    return render_template('dateChooser.html')

@app.route('/', methods=["POST"])
@login_required
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
@login_required
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

# somewhere to login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template('master.html')


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return Response('<p>Logged out</p>')


# handle login failed
@app.errorhandler(401)
def page_not_found(e):
    return Response('<p>Login failed</p>')


# callback to reload the user object
@login_manager.user_loader
def load_user(usr):
    return User(usr, usr)

    
if __name__ == '__main__':
    app.run()

