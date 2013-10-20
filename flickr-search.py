# encoding: utf-8
from urllib import urlopen, urlencode
import json

API_KEY = 'a7c95c75787dacab6e0525735f18982b'
URL = 'http://api.flickr.com/services/rest'

params = {
	'api_key': API_KEY,
	'method': 'flickr.photos.search',
	'format': 'json',
	'nojsoncallback': 1,
	'text': 'owl'
}

query_string = '?{}'.format(urlencode(params))
request_url = ''.join((URL, query_string))

response_str = urlopen(request_url).read()
with open('ex.json', 'w') as f:
	f.write(response_str)
response = json.loads(response_str)
print len(response['photos']['photo'])
for k in response['photos']:
	print k