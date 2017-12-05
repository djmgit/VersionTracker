from main import db

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
