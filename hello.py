from flask import (
    Flask, url_for, request, render_template, jsonify,
    make_response, abort, redirect, session
)
from markupsafe import escape

app = Flask(__name__)


# @app.route("/")
# def index():
#     return "this is home page"

@app.route("/hello/")
def hello_world():
    return "hello world of flask 123"

# variables rule
@app.route("/user/<username>/")
def username(username):
    return "hello %s" %escape(username)

@app.route("/int_demo/<int:int_var>/")
def int_demo(int_var):
    return "number in url is %d"%int_var

@app.route("/path_demo/<path:mypath>/")
def path_demo(mypath):
    return "path in url is %s" %escape(mypath)

# URL Bining
with app.test_request_context():
    # print(url_for('index'))
    print(url_for('hello_world'))
    print(url_for('username', username='vis'))
    print(url_for('int_demo', int_var=15))


# Http methods
@app.route("/login_method_test/", methods=['GET', 'POST'])
def login_method_test():
    if request.method == 'POST':
        return 'logged in using post method'
    else:
        return 'logged in using get method'

# url_for('static', filename='style.css')  # wip

@app.route('/custom_template/')
@app.route('/custom_template/<username>/')
def custom_template(username):
    return render_template('custom_template.html', username=username)

# access request data
with app.test_request_context("/hello/", method='POST'):
    assert request.path == '/hello/'
    assert request.method == "POST"
    # print(request.method)

@app.route("/login_post/", methods=['POST', 'GET'])
def login_post():
    if request.method == 'POST':
        print(request.form.get('username'))
        username = request.form.get('username')
    else:
        username = request.args.get('username')
    return username# jsonify(request.json)

@app.route("/form/", methods=['GET'])
def form():
    return render_template('form.html')


# Using cookies
@app.route("/set_cookie/")
def set_cookie():
    res = make_response(render_template('cookie.html'))
    res.set_cookie('username', 'vis') # setting cookie value
    return res

@app.route("/get_cookie/")
def get_cookie():
    username = request.cookies.get('username') # getting cookie value
    return username

# redirects and errors
@app.route("/redirect_to_hello/")
def redirect_to_hello():
    return redirect(url_for('hello_world'))

@app.route('/abort_demo/')
def abort_demo():
    abort(404)
    print("this will never print")
    return 'response'

@app.errorhandler(404)
def page_not_found_error(error):
    return render_template('page_not_found_template.html'), 404

# returning simple json
@app.route("/me/")
def me_api():
    # user = get_current_user()
    return {
        "username": 'user.username',
        "theme": 'user.theme',
        "image": 'user.image' # url_for("user_image", filename=user.image),
    }
@app.route("/dict_as_json/")
def dict_as_json():
    mydict = {
        'name': 'vis',
        'age': 25,
        'win': True
    }
    return jsonify(mydict)
    # return mydict # this also works

# session
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():
    if 'username' in session:
        return "logged in as %s"%escape(session['username'])
    return "You are not logged in"

@app.route("/login/", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form.get('username')
        return redirect(url_for('index'))
    return '''
    <form method='post'>
        <p><input type=text name='username'>
        <p><input type=submit value='login'>
    </form>
    '''

@app.route("/logout/")
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
