import logging

from badpoetry.lib.base import *

log = logging.getLogger(__name__)

class PoemController(BaseController):
	def index(self):
		return render('/poems/index.mako')
	
	def add(self):
		pass