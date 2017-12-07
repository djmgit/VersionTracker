from flask import Flask, redirect, url_for, request, jsonify, render_template
from VersionScraper import get_versions
from AlternateScraper import get_alternatives
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
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

db.create_all();

class AdminAdd(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        if request.method == 'POST':
            name = request.form['name']
            versions = request.form['versions']
            num_of_ver = request.form['numversions']
            initial_release = request.form['initialrelease']

            versions_list = versions.split(',')
            versions_list = [ver.strip() for ver in versions_list]
            soft_obj = VersionDB(name, json.dumps(versions_list), int(num_of_ver), initial_release)
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

admin = Admin(app, name='VersionTracker', template_mode='bootstrap3')
admin.add_view(AdminAdd(name='Add software', endpoint='adminadd'))
admin.add_view(VersionDBView(VersionDB, db.session))

def get_response(software, version):
    item = VersionDB.query.filter_by(name=software).all()
    print (item)
    if len(item) == 0:
        response = get_versions('_'.join(software.split()))
        if (response['found'] == 'NOT_FOUND'):
            return -1
        soft_obj = VersionDB(software, json.dumps(response['versions']), response['number_of_versions'], response['initial_release'])
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
    response['versions'] = json.loads(soft.versions)
    response['latest_version'] = response['versions'][0]
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
