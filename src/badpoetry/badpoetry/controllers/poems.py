import logging

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class PoemsController(BaseController):
	def __init__(self):
		g.tags = model.Tag().all().order('-count').order('tag').fetch(limit=10)
	
	def index(self):
		#query = db.Query(model.Poem)
		c.poems = model.Poem.all().order('-created')
		return render('/poems/index.mako')
	
	def create(self):
		return render('/poems/create.mako')
	
	def add(self):
		p = model.Poem()
		p.title = request.POST.get('title')
		p.content = request.POST.get('content')
		p.tags = request.POST.get('tags').split(' ')
		p.put()

		for tag in p.tags:
			t = model.Tag.all().filter('tag = ', tag).get()
			if t:
				t.count = t.count + 1
			else:
				t = model.Tag(tag=tag, count=1)
			t.put()
			
		redirect_to('/')
	
