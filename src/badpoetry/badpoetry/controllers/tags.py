import logging

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class TagsController(BaseController):
	def show(self, id):
		#query = db.Query(model.Poem)
		c.poems = model.Poem.all().filter("tags = ", id)
		return render('/poems/index.mako')
	
