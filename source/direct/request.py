
import json
import requests

from .response import response


class request():
	def __init__(self, *, data, method, service, token, language=None):
		self.url = 'https://api.direct.yandex.com/json/v5/' + service.lower()
		self.headers = {
			'Accept': None,
			'Accept-Encoding': None,
			'Authorization': 'Bearer ' + token,
			'Connection': None,
			'User-Agent': None,
		}
		if language:
			self.headers['Accept-Language'] = language
		self.json = {
			'method': method,
			'params': data,
		}
	def send(self):
		data = requests.post(**{
			'url': self.url,
			'headers': self.headers,
			'data': json.dumps(**{
				'obj': self.json,
				'ensure_ascii': False,
				'separators': (',', ':'),
			}).encode(),
		})
		return response(data)


if __name__ == '__main__':
	import os
	request = request(**{
		'token': os.environ.get('token'),
		'service': 'campaigns',
		'method': 'get',
		'data': {
			'SelectionCriteria': {
			},
			'FieldNames': [
				'Id',
			],
		},
	})
	response = request.send()
