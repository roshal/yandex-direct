from .request import request
class method():
	def __init__(self, *, method, service, token, language=None):
		self.method = method
		self.service = service
		self.token = token
		self.language = language
	def request(self, data):
		return request(**{
			'data': data,
			'method': self.method,
			'service': self.service,
			'token': self.token,
			'language': self.language,
		})
if __name__ == '__main__':
	import os
	service = method(**{
		'token': os.environ.get('token'),
		'service': 'campaigns',
		'method': 'get',
	})
	method = service.request({
		'SelectionCriteria': {
		},
		'FieldNames': [
			'Id',
		],
	})
