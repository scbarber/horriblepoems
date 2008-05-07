import logging
from datetime import datetime, timedelta
from google.appengine.api import users

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class PoemsController(BaseController):
	def index(self):
		#query = db.Query(model.Poem)
		c.poems = model.Poem.all().order('-created')
		return render('/poems/index.mako')
	
	def today(self):
		d = datetime.today().date()
		today = datetime(d.year, d.month, d.day)
		c.poems = model.Poem.all().filter('created > ', today)
		c.title = "today's poems"
		return render('/poems/index.mako')
	
	def week(self):
		today = datetime.today().date()
		
		d = today - timedelta(today.isoweekday())
		back = datetime(d.year, d.month, d.day)
		
		d = today + timedelta(7 - today.isoweekday())
		forward = datetime(d.year, d.month, d.day)
		c.poems = model.Poem.all().filter('created > ', back).filter('created < ', forward)
		c.title = "this week's poems"
		return render('/poems/index.mako')
	
	def month(self):
		d = datetime.today().date()
		back = datetime(d.year, d.month, 1)
		forward = datetime(d.year, d.month+1, 1)
		c.poems = model.Poem.all().filter('created > ', back).filter('created < ', forward)
		c.title = "this month's poems"
		return render('/poems/index.mako')
	
	def create(self):
		user = users.get_current_user()
		if user:
			return render('/poems/create.mako')
		else:
			redirect_to(users.create_login_url('/create'))
	
	def add(self):
		p = model.Poem()
		p.title = request.POST.get('title')
		p.content = request.POST.get('content')
		p.tags = request.POST.get('tags').split(' ')
		p.author = users.get_current_user()
		p.put()

		for tag in p.tags:
			t = model.Tag.all().filter('tag = ', tag).get()
			if t:
				t.count = t.count + 1
			else:
				t = model.Tag(tag=tag, count=1)
			t.put()
			
		redirect_to('/')
	
