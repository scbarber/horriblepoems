from badpoetry.tests import *

class TestAuthorsController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='authors'))
        # Test response...
