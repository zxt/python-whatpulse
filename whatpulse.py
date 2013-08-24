import urllib, urllib2
import json

# API Documentation: http://whatpulse.org/pages/webapi/

class API:

    def __init__(self):
        self.base_url = 'http://api.whatpulse.org'

    def _make_request(self, url, params):
        if params:
            url = url + '?' + urllib.urlencode(params)

        fp = urllib2.urlopen(url, timeout=5)
        # errors (eg., unknown user id) are returned in XML, not JSON
        # if we can't decode response as JSON, assume error response
        try:
            stats = json.load(fp)
        except ValueError:
            stats = {}
        return stats

    def get_user(self, user):
        api_url = self.base_url + '/user.php'

        params = {'user': user, 'format': 'json'}

        return self._make_request(api_url, params)

    def get_team(self, team, members=False):
        api_url = self.base_url + '/team.php'

        params = {'team': team, 'format': 'json'}
        if members:
            params['members'] = 'yes'

        return self._make_request(api_url, params)
    
    def get_pulses(self, user=None, team=None):
        api_url = self.base_url + '/pulses.php'

        params = {'format': 'json'}
        if user is not None:
            params['user'] = user
        elif team is not None:
            params['team'] = team 
        else:
            return {}

        stats = self._make_request(api_url, params)

        # for some reason the pulses API does return errors in JSON as asked, unlike the other APIs
        # yay inconsistency
        if stats.get('error') is not None:
            return {} 
        else:
            return stats
