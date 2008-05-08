import logging

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class TagsController(BaseController):
	def index(self):
		c.tags = model.Tags.all().order('-count').order('tag')
		return render('/tags/index.mako')
	
	def show(self, id):
		#query = db.Query(model.Poem)
		c.poems = model.Poems.all().filter("tags = ", id)
		return render('/poems/index.mako')
	
