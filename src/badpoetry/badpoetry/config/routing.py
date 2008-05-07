"""Routes configuration

The more specific and detailed routes should be defined first so they
may take precedent over the more generic routes. For more information
refer to the routes manual at http://routes.groovie.org/docs/
"""
from pylons import config
from routes import Mapper

def make_map():
	"""Create, configure and return the routes Mapper"""
	map = Mapper(directory=config['pylons.paths']['controllers'],
	             always_scan=config['debug'])
	
	# The ErrorController route (handles 404/500 error pages); it should
	# likely stay at the top, ensuring it can always be resolved
	map.connect('error/:action/:id', controller='error')
	
	# CUSTOM ROUTES HERE
	map.connect('/', controller='poems', action='index')
	map.connect('/create', controller='poems', action='create')
	map.connect('/today', controller='poems', action='today')
	map.connect('/week', controller='poems', action='week')
	map.connect('/month', controller='poems', action='month')
	
	map.connect(':controller/:action/:id')
	map.connect('*url', controller='template', action='view')
	
	return map
