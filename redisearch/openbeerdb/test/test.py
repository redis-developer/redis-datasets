import redis
import unittest
import requests

r = redis.Redis(host='localhost', port=6379, db=0)

class SearchBeerTest(unittest.TestCase):

    def testRediSearch(self):
        """Test RediSearch beer data"""
        r = redis.Redis(host='localhost', port=6379, db=0)
        r.client_setname(self._testMethodName)
        
        res = r.execute_command('FT.SEARCH', 'beerIdx', '@category:Irish Ale|German Ale @abv:[9 inf]')
        self.assertEquals(len(res), 7)
        
        res = r.execute_command('FT.SEARCH', 'beerIdx', '@abv:[5 6]')
        self.assertEquals(len(res), 21)

        res = r.execute_command('FT.SEARCH', 'breweryIdx', '@location:[-87.623177 41.881832 10 km]')
        self.assertEquals(len(res), 17)

    def testFrontend(self):
        """Test Frontend"""
        
        res = requests.get('http://localhost:5000')
        self.assertEquals(res.status_code, 200)        

if __name__ == '__main__':
    unittest.main()
