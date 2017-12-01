from flask import Flask, redirect, url_for, request, jsonify
from VersionScraper import get_versions
from flask_sqlalchemy import SQLAlchemy
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///versions.sqlite3'
app.config['SECRET_KEY'] = "THIS IS SECRET"

db = SQLAlchemy(app)

class VersionDB(db.Model):
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

def get_response(software, version):
	item = VersionDB.query.filter_by(name=software).all()
	print (item)
	if len(item) == 0:
		response = get_versions('_'.join(software.split()))
		soft_obj = VersionDB(software, json.dumps(response['versions']), response['number_of_versions'], response['initial_release'])
		db.session.add(soft_obj)
		db.session.commit()
		item = VersionDB.query.filter_by(name=software).all()[0]
	else:
		item = item[0]
	return item

@app.route('/version_track')
def version_track():
	software = request.args.get('name')
	version = request.args.get('version')

	print (software, version)
	soft = get_response(software, version)

	response = {}
	response['status'] = 'FOUND'
	response['name'] = soft.name
	response['number_of_versions'] = soft.num_of_ver
	response['versions'] = json.loads(soft.versions)
	response['initial_release'] = soft.initial_release
	
	return jsonify(response)

if __name__ == "__main__":
	db.create_all()
	app.run(host='0.0.0.0', debug=True)
