from badpoetry.tests import *

class TestPoemController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='poem'))
        # Test response...
