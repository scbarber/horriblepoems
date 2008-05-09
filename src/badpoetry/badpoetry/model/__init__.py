from google.appengine.ext import db

class Poems(db.Model):
	author = db.UserProperty()
	title = db.StringProperty(unicode)
	content = db.TextProperty(unicode)
	tags = db.ListProperty(unicode)
	rating = db.FloatProperty() # 3.4 stars
	total_ratings = db.IntegerProperty() # 17
	number_of_ratings = db.IntegerProperty() # 5
	favorited = db.IntegerProperty() # 3 (3 people marked this as a favourite)
	created = db.DateTimeProperty(auto_now_add=True)

class Tags(db.Model):
	tag = db.StringProperty(unicode)
	count = db.IntegerProperty()

class UserMetadata(db.Model):
	user = db.UserProperty()
	poem_count = db.IntegerProperty()
	favourites = db.ListProperty(db.Key)
	poems_rated = db.ListProperty(db.Key)

# Validation Schtuff
import formencode

class PoemForm(formencode.Schema):
	allow_extra_fields = True
	filter_extra_fields = True
	title = formencode.validators.UnicodeString(not_empty=True)
	content = formencode.validators.UnicodeString(not_empty=True)
