import logging
import paginate
from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class TagsController(BaseController):
	def index(self):
		c.tags = model.Tags.all().order('-count').order('tag')
		return render('/tags/index.mako')
	
	def show(self, id):
		poems = model.Poems.all().filter("tags = ", id)
		page = request.GET.get('page_nr') or 1
		c.poems = paginate.Page([poem for poem in poems], items_per_page=10, current_page=page)
		c.title = "poems tagged with '%s'" % (id)
		return render('/poems/index.mako')
	
