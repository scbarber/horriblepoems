from badpoetry.tests import *

class TestPoemsController(TestController):

    def test_index(self):
        response = self.app.get(url_for(controller='poems'))
        # Test response...
