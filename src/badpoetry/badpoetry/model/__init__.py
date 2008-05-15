from google.appengine.ext import db
from google.appengine.api import users

class Poems(db.Model):
	author = db.UserProperty()
	title = db.StringProperty(unicode)
	content = db.TextProperty(unicode)
	tags = db.ListProperty(db.Category)
	score = db.IntegerProperty()
	scored_by = db.ListProperty(users.User)
	favourites = db.ListProperty(users.User)
	number_of_favourites = db.IntegerProperty(default=0)
	created = db.DateTimeProperty(auto_now_add=True)

class Tags(db.Model):
	tag = db.StringProperty(unicode)
	count = db.IntegerProperty()

class UserMetadata(db.Model):
	user = db.UserProperty()
	poem_count = db.IntegerProperty()
	score = db.IntegerProperty()

class Ratings(db.Model):
	poem = db.ReferenceProperty()
	user = db.UserProperty()
	score = db.IntegerProperty()

# Validation Schtuff
import formencode

class PoemForm(formencode.Schema):
	allow_extra_fields = True
	filter_extra_fields = True
	title = formencode.validators.UnicodeString(not_empty=True)
	content = formencode.validators.UnicodeString(not_empty=True)
