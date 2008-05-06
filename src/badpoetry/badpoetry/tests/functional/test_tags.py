from badpoetry.tests import *

class TestTagsController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='tags'))
        # Test response...
