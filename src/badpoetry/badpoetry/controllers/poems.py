import logging

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class PoemsController(BaseController):
	def index(self):
		#query = db.Query(model.Poem)
		c.poems = model.Poem.all()
		return render('/poems/index.mako')
	
	def create(self):
		return render('/poems/create.mako')
	
	def add(self):
		p = model.Poem()
		p.title = request.POST.get('title')
		p.content = request.POST.get('content')
		p.tags = request.POST.get('tags').split(' ')
		p.put()
		redirect_to('/')
	
