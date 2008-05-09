import logging
import paginate
from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class AuthorsController(BaseController):
	def index(self):
		c.authors = model.UserMetadata.all().order('-poem_count').order('user')
		return render('/authors/index.mako')
	
