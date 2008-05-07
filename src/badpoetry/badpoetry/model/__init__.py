from google.appengine.ext import db

class Poem(db.Model):
	author = db.UserProperty()
	title = db.StringProperty()
	content = db.TextProperty()
	tags = db.ListProperty(unicode)
	created = db.DateTimeProperty(auto_now_add=True)

class Tag(db.Model):
	count = db.IntegerProperty()