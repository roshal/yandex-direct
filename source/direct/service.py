from .method import method
class service():
	def __init__(self, *, service, token, language=None):
		self.service = service
		self.token = token
		self.language = language
	def method(self, name):
		return method(**{
			'method': name,
			'service': self.service,
			'token': self.token,
			'language': self.language,
		})
if __name__ == '__main__':
	import os
	service = service(**{
		'token': os.environ.get('token'),
		'service': 'campaigns',
	})
	request = service.method('get')
