import logging
from datetime import datetime, timedelta
import paginate

from google.appengine.ext import db
from google.appengine.api import users

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

def page_this(poems):
	page = request.GET.get('page_nr') or 1
	return(paginate.Page([poem for poem in poems], items_per_page=10, current_page=page))

class PoemsController(BaseController):
	def index(self):
		c.poems = page_this(model.Poems.all().order('-created'))
		return render('/poems/index.mako')
	
	def show(self, id):
		poem = model.Poems.get(id)
		c.title = poem.title
		c.poems = [poem] # This is a hack to make c.poems iterable so I don't have to change the template
		return render('/poems/index.mako')
	
	def today(self):
		d = datetime.today().date()
		today = datetime(d.year, d.month, d.day)
		c.poems = page_this(model.Poems.all().filter('created > ', today))
		c.title = "today's poems"
		return render('/poems/index.mako')
	
	def week(self):
		today = datetime.today().date()
		
		d = today - timedelta(today.isoweekday())
		back = datetime(d.year, d.month, d.day)
		
		d = today + timedelta(7 - today.isoweekday())
		forward = datetime(d.year, d.month, d.day)
		c.poems = page_this(model.Poems.all().filter('created > ', back).filter('created < ', forward))
		c.title = "this week's poems"
		return render('/poems/index.mako')
	
	def month(self):
		d = datetime.today().date()
		back = datetime(d.year, d.month, 1)
		forward = datetime(d.year, d.month+1, 1)
		c.poems = page_this(model.Poems.all().filter('created > ', back).filter('created < ', forward))
		c.title = "this month's poems"
		return render('/poems/index.mako')
	
	def create(self):
		if self.user:
			return render('/poems/create.mako')
		else:
			redirect_to(users.create_login_url('/create'))
	
	def edit(self, id):
		poem = model.Poems.get(id)
		if self.user != poem.author:
			session['flash'] = "You can only edit your own poems."
			session.save()
			send_back()
		c.poem = poem
		c.title = poem.title
		return render('/poems/edit.mako')
	
	@validate(schema=model.PoemForm(), form='create')
	def add(self):
		if self.user == None:
			redirect_to(users.create_login_url('/create'))
			return None
		p = model.Poems()
		p.title = request.POST.get('title')
		p.content = request.POST.get('content')
		p.tags = [db.Category(tag.strip()) for tag in request.POST.get('tags').lower().split(',')]
		p.author = self.user
		p.put()
		
		for tag in p.tags:
			t = model.Tags.all().filter('tag = ', tag).get()
			if t:
				t.count = t.count + 1
			else:
				t = model.Tags(tag=tag, count=1)
			t.put()
		
		userMeta = model.UserMetadata.all().filter('user = ', self.user).get()
		if userMeta:
			userMeta.poem_count += 1
		else:
			userMeta = model.UserMetadata(user=self.user, poem_count=1)
		userMeta.put()
		redirect_to('/')
	
 	@validate(schema=model.PoemForm(), form='edit')
	def update(self, id):
		poem = model.Poems.get(id)
		if self.user != poem.author:
			session['flash'] = "You can only edit your own poems."
			session.save()
			send_back()
		poem.title = self.form_result.get('title')
		poem.content = self.form_result.get('content')
		
		# The following two loops will find all changed tags and account for them
		tags = [tag.strip() for tag in request.POST.get('tags').lower().split(',')]
		for t in poem.tags:
			if not t in tags:
				tag = model.Tags.all().filter('tag = ', t).get()
				Tags.count = Tags.count - 1
				if Tags.count == 0:
					Tags.delete()
				else:
					Tags.put()
			else:
				tags.remove(t)

		for tag in tags:
			t = model.Tags.all().filter('tag = ', tag).get()
			if t:
				t.count = t.count + 1
			else:
				t = model.Tags(tag=tag, count=1)
			t.put()
		poem.tags = [db.Category(tag.strip()) for tag in request.POST.get('tags').lower().split(',')]
		poem.put()
		redirect_to(h.url_for(action="show", id=poem.key()))
	
	def delete(self, id):
		poem = model.Poems.get(id)
		if self.user != poem.author:
			session['flash'] = "You can only delete your own poems."
			session.save()
			send_back()
		for t in poem.tags:
			tag = model.Tags.all().filter('tag = ', t).get()
			Tags.count = Tags.count - 1
			if Tags.count == 0:
				Tags.delete()
			else:
				Tags.put()
		poem.delete()
		
		userMeta = model.UserMetadata.all().filter('user = ', self.user).get()
		if userMeta:
			userMeta.poem_count -= 1
			userMeta.put()
		redirect_to("/")
	
	def author(self, id):
		user = model.UserMetadata.get(id)
		c.poems = page_this(model.Poems.all().filter('author = ', user.user).order('-created'))
		c.title = "poems by %s" % (user.user.nickname())
		return render('/poems/index.mako')
	
	def mine(self):
		if not self.user:
			redirect_to(users.create_login_url(url_for(controller="poems", action="mine")))
		else:
			c.poems = page_this(model.Poems.all().filter('author = ', self.user).order('-created'))
			c.title = "your poems"
			return render('/poems/index.mako')
	
	def rss(self):
		d = datetime.today().date() - timedelta(3) # Last 3 days worth of poems.
		date = datetime(d.year, d.month, d.day)
		c.poems = page_this(model.Poems.all().filter('created > ', date))
		response.headers['content-type'] = 'application/rss+xml'
		return render('/rss2.mako')
	
	def favourite(self, id):
		if self.user == None: return None
		poem = model.Poems.get(id)
		if self.user in poem.favourites:
			poem.favourites.remove(self.user)
			poem.number_of_favourites -= 1
		else:
			poem.favourites.append(self.user)
			poem.number_of_favourites += 1
		poem.put()
		return None
	
	def favourites(self):
		if not self.user:
			redirect_to(users.create_login_url(url_for(controller="poems", action="favourites")))
		else:
			c.poems = page_this(model.Poems.all().filter('favourites = ', self.user).order('-created'))
			c.title = "your favourite poems"
			return render('/poems/index.mako')
	
	def put(self):
		self.user = users.User(request.POST.get('author'))
		p = model.Poems()
		p.title = request.POST.get('title')
		p.content = request.POST.get('content')
		p.tags = [db.Category(tag.strip()) for tag in request.POST.get('tags').lower().split(',')]
		p.author = self.user
		p.created = datetime.fromtimestamp(request.POST.get('created_at'))
		p.put()

		for tag in p.tags:
			t = model.Tags.all().filter('tag = ', tag).get()
			if t:
				t.count = t.count + 1
			else:
				t = model.Tags(tag=tag, count=1)
			t.put()

		userMeta = model.UserMetadata.all().filter('user = ', self.user).get()
		if userMeta:
			userMeta.poem_count += 1
		else:
			userMeta = model.UserMetadata(user=self.user, poem_count=1)
		userMeta.put()
		redirect_to('/')
	
