from google.appengine.ext import db

class Poem(db.Model):
	author = db.UserProperty()
	title = db.StringProperty(unicode)
	content = db.TextProperty(unicode)
	tags = db.ListProperty(unicode)
	rating = db.FloatProperty() # 3.4 stars
	total_ratings = db.IntegerProperty() # 17
	number_of_ratings = db.IntegerProperty() # 5
	favorited = db.IntegerProperty() # 3 (3 people marked this as a favourite)
	created = db.DateTimeProperty(auto_now_add=True)

class Tag(db.Model):
	tag = db.StringProperty(unicode)
	count = db.IntegerProperty()