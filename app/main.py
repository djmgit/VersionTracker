from flask import Flask, redirect, url_for, request, jsonify, render_template
from VersionScraper import get_versions
from AlternateScraper import get_alternatives
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_login import LoginManager, login_user, login_required, logout_user
import json
import re
import os

app = Flask(__name__)
if os.environ.get('DATABASE_URL') is None:
    #app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/deep'
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SECRET_KEY'] = "THIS IS SECRET"

db = SQLAlchemy(app)

class VersionDB(db.Model):
    __tablename__ = 'versiondb'

    id = db.Column('software_id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    versions = db.Column(db.String)
    num_of_ver = db.Column(db.Integer)
    initial_release = db.Column(db.String)

    def __init__(self, name, versions, num_of_ver, initial_release):
        self.name = name
        self.versions = versions
        self.num_of_ver = num_of_ver
        self.initial_release = initial_release

class SimilarSoftwares(db.Model):
    __tablename__ = 'similar_softwares'

    id = db.Column('software_id', db.Integer, primary_key=True)
    name = db.Column(db.String)
    alternatives = db.Column(db.String)

    def __init__(self, name, alternatives):
        self.name = name
        self.alternatives = alternatives

class User(db.Model):
    __tablename__ = "users"

    email = db.Column(db.String(80), primary_key=True, unique=True)
    password = db.Column(db.String(80))
    def __init__(self, email, password):
        self.email = email
        self.password = password
    def __repr__(self):
        return '<User %r>' % self.email
    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.email)

db.create_all();

class AdminAdd(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            print(request.form)
            name = request.form['name'].strip()
            versions = request.form['versions'].strip()
            num_of_ver = request.form['numversions'].strip()
            initial_release = request.form['initialrelease'].strip()
            similar_softwares = request.form['similar-softwares'].strip()

            versions_list = versions.split(',')
            versions_list = [ver.strip() for ver in versions_list]
            soft_obj = VersionDB(name, versions, int(num_of_ver), initial_release)
            db.session.add(soft_obj)
            db.session.commit()
            soft_obj = SimilarSoftwares(name, similar_softwares)
            db.session.add(soft_obj)
            db.session.commit()
            return self.render('admin-add.html')
        else:
            return self.render('admin-add.html')

class VersionDBView(ModelView):
    can_create = False
    can_view_details = True
    column_searchable_list = ['name']
    edit_modal = True
    column_exclude_list = ['versions']
    column_filters = ['name']

class SimilarSoftwaresDBView(ModelView):
    can_create = False
    column_searchable_list = ['name', 'alternatives']
    edit_modal = True
    column_filters = ['name']

class UserDBView(ModelView):
    can_create = False
    column_searchable_list = ['email']


# setup admin
admin = Admin(app, name='VersionTracker', template_mode='bootstrap3')
admin.add_view(AdminAdd(name='Add software', endpoint='adminadd'))
admin.add_view(VersionDBView(VersionDB, db.session))
admin.add_view(SimilarSoftwaresDBView(SimilarSoftwares, db.session))
admin.add_view(UserDBView(User, db.session))

# setup authentication
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(email):
    return User.query.filter_by(email=email).first()

def get_response(software, version):
    item = VersionDB.query.filter_by(name=software).all()
    print (item)
    if len(item) == 0:
        response = get_versions('_'.join(software.split()))
        if (response['found'] == 'NOT_FOUND'):
            return -1
        soft_obj = VersionDB(software, ",".join(response['versions']), response['number_of_versions'], response['initial_release'])
        db.session.add(soft_obj)
        db.session.commit()
        item = VersionDB.query.filter_by(name=software).all()[0]
    else:
        item = item[0]
    return item

def store_alternatives(software):
    item = SimilarSoftwares.query.filter_by(name=software).all()
    print (item)
    if len(item) == 0:
        response = get_alternatives(software)
        response_final = []
        for r in response:
            r = r.strip()
            if r != '':
                response_final.append(r)
        soft_obj = SimilarSoftwares(software, ','.join(response_final))
        db.session.add(soft_obj)
        db.session.commit()
        item = SimilarSoftwares.query.filter_by(name=software).all()[0]
    else:
        item = item[0]
    return item

def get_pos(response, ver):
    regex = re.compile(r'[^\d.]+')
    versions = response['versions']
    versions = [regex.sub('', version) for version in versions]

    for index in range(len(versions)):
        if versions[index] == ver or versions[index].startswith(ver):
            return index + 1
    return -1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contribute', methods=('GET', 'POST'))
@login_required
def contribute():
    print (request.method)
    if request.method == 'POST':
        name = request.form['name'].strip()
        versions = request.form['versions'].strip()
        num_of_ver = request.form['numversions'].strip()
        initial_release = request.form['initialrelease'].strip()
        similar_softwares = request.form['similar-softwares'].strip()

        soft_obj = VersionDB(name, versions, int(num_of_ver), initial_release)
        db.session.add(soft_obj)
        db.session.commit()
        soft_obj = SimilarSoftwares(name, similar_softwares)
        db.session.add(soft_obj)
        db.session.commit()
        return render_template('contribute.html')
    else:
        return render_template('contribute.html')

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(email=email).first():
            return render_template('signup.html')
            # handle duplicate user case
        else:
            print (email, password)
            newuser = User(email, password)
            db.session.add(newuser)
            db.session.commit()
            # login user
            login_user(newuser)
            return redirect(url_for('index'))
    else:
        return render_template('signup.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            if user.password == password:
                print ('successfully logged in')
                # login user
                login_user(user)
                return redirect(url_for('index'))
            else:
                # show error
                print ('wronng password')
                return render_template('login.html')
        else:
            # user not found
            return render_template('login.html')
    else:
        return render_template('login.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/version_track/api')
def version_track():
    software = request.args.get('name')
    version = request.args.get('version')

    print (software, version)
    soft = get_response(software, version)

    response = {}
    if soft == -1:
        response['software_found'] = 'NOT_FOUND'
        return jsonify(response)
    response['software_found'] = "FOUND"
    response['name'] = soft.name
    response['number_of_versions'] = soft.num_of_ver
    versions = soft.versions.split(',')
    versions = [ver.strip() for ver in versions]
    response['versions'] = versions
    response['latest_version'] = versions[0]
    response['initial_release'] = soft.initial_release
    response['similar_softwares'] = store_alternatives(software).alternatives.split(',')

    pos = get_pos(response, version)
    if pos == -1:
        response['version_found'] = "NOT_FOUND"
        return jsonify(response)
    response['version_found'] = "FOUND"

    response['num_of_new_versions'] = pos - 1

    if (pos - 1 >= 5):
        response['is_obsolete'] = "OBSOLETE"
    else:
        response['is_obsolete'] = "NOT_OBSOLETE"

    return jsonify(response)

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
