import logging
from badpoetry.lib import paginate
from badpoetry.lib.base import *
from google.appengine.ext import db
from urllib import unquote_plus

log = logging.getLogger(__name__)

class Bunch:
	def __init__(self, **kwds):
		self.__dict__.update(kwds)

def inc_string(string, allowGrowth=True):
	'''Increment a string.'''
	CHAR_RANGES = [
				   Bunch(from_char=ord('0'), to_char=ord('9')), # digits
				   Bunch(from_char=ord('A'), to_char=ord('Z')), # upper case
				   Bunch(from_char=ord('a'), to_char=ord('z')), # lower case
				  ]
	string_chars = list(string)
	string_chars[-1] = chr(ord(string_chars[-1]) + 1)
	for index in range(-1, -len(string_chars), -1):
		for char_range in CHAR_RANGES:
			if ord(string_chars[index]) == char_range.to_char + 1:
				string_chars[index] = chr(char_range.from_char)
				string_chars[index-1] = chr(ord(string_chars[index-1]) + 1)
	for char_range in CHAR_RANGES:
		if ord(string_chars[0]) == char_range.to_char + 1:
			if allowGrowth:
				string_chars[0] = chr(char_range.from_char)
				string_chars.insert(0, chr(char_range.from_char))
			else:
				raise ValueError, string + " cannot be incremented."
	return ''.join(string_chars)


class TagsController(BaseController):
	def index(self):
		c.tags = model.Tags.all().order('-count').order('tag')
		return render('/tags/index.mako')
	
	def show(self, id):
		id = unquote_plus(id)
		poems = model.Poems.all().filter("tags = ", db.Category(id))
		page = request.GET.get('page_nr') or 1
		c.poems = paginate.Page([poem for poem in poems], items_per_page=10, current_page=page)
		c.title = "poems tagged with '%s'" % (id)
		return render('/poems/index.mako')
	
	def suggest(self):
		tag = request.params.get('tag')
		if not tag: return None
		c.tags = model.Tags.all().filter('tag >= ', tag).filter('tag <= ', inc_string(tag))
		return render('/tags/suggest.mako')
	
