import json
class response():
	def __init__(self, response):
		self.response = response
		self.status_code = response.status_code
		self.json = response.json
	def get_json_request_headers(self):
		return json.dumps(**{
			'obj': dict(self.response.request.headers),
			'indent': 2,
			'sort_keys': True,
		})
	def get_json_request(self):
		return json.dumps(**{
			'obj': json.loads(self.response.request.body),
			'indent': 2,
			'ensure_ascii': False,
			'sort_keys': True,
		})
	def get_json_headers(self):
		return json.dumps(**{
			'obj': dict(self.response.headers),
			'indent': 2,
			'sort_keys': True,
		})
	def get_json(self):
		return json.dumps(**{
			'ensure_ascii': False,
			'indent': 2,
			'obj': self.response.json(),
			'sort_keys': True,
		})
	def debug(self):
		if self.response.status_code != 200 or self.response.json().get('error', False):
			print('Произошла ошибка при обращении к серверу API Директа.')
			print('Код ошибки: {}'.format(self.response.json()['error']['error_code']))
			print('Описание ошибки: {}'.format(self.response.json()['error']['error_detail']))
			print('RequestId запроса: {}'.format(self.response.headers.get('RequestId', False)))
		else:
			print('RequestId запроса: {}'.format(self.response.headers.get('RequestId', False)))
			print('Информация о баллах: {}'.format(self.response.headers.get('Units', False)))
			for campaign in self.response.json()['result']['Campaigns']:
				print('Рекламная кампания: {} №{}'.format(campaign['Name'], campaign['Id']))
			if self.response.json()['result'].get('LimitedBy', False):
				print('Получены не все доступные объекты.')
	def print(self):
		print(self.get_json_request_headers())
		print(self.get_json_request())
		print(self.get_json_headers())
		print(self.get_json())
