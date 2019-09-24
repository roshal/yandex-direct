from .service import service
class api():
	def __init__(self, *, token, language=None):
		self.token = token
		self.language = language
	def service(self, name):
		return service(**{
			'service': name,
			'token': self.token,
			'language': self.language,
		})
if __name__ == '__main__':
	import os
	api = api(**{
		'token': os.environ.get('token'),
	})
	service = api.service('campaigns')
