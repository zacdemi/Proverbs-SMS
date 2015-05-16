import unittest
from datetime import datetime, timedelta
import development

class testRunOut(unittest.testCase):
   
    #base date will be 1/1/2015
    def test_runout_date(self):
        result = development.runout_date([1,2,3,4],40)
        self.assertEqual("2015-01-29",result)


