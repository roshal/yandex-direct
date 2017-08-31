import json
import os
import requests
class request():
	def __init__(self, *, url, language, token):
		self.url = url
		self.headers = {
			'Accept-Language': language,
			'Authorization': 'Bearer ' + token,
		}
		self.url = 'https://api-sandbox.direct.yandex.com/json/v5/campaigns'
		self.json = {
			'method': 'get',
			'params': {
				'SelectionCriteria': {
				},
				'FieldNames': [
					'Id',
				],
			},
		}
	def main(self):
		body = json.dumps(self.body, ensure_ascii=False)
		result = requests.post(self.url, body, headers=self.headers)
		print(json.dumps(dict(result.request.headers), indent=2))
		print(json.dumps(json.loads(result.request.body), ensure_ascii=False, indent=2))
		print(json.dumps(dict(result.headers), indent=2))
		print(json.dumps(result.json(), ensure_ascii=False, indent=2))
		if result.status_code != 200 or result.json().get('error', False):
			print('Произошла ошибка при обращении к серверу API Директа.')
			print('Код ошибки: {}'.format(result.json()['error']['error_code']))
			print('Описание ошибки: {}'.format(result.json()['error']['error_detail']))
			print('RequestId запроса: {}'.format(result.headers.get('RequestId', False)))
		else:
			print('RequestId запроса: {}'.format(result.headers.get('RequestId', False)))
			print('Информация о баллах: {}'.format(result.headers.get('Units', False)))
			for campaign in result.json()['result']['Campaigns']:
				print('Рекламная кампания: {} №{}'.format(campaign['Name'], campaign['Id']))
			if result.json()['result'].get('LimitedBy', False):
				print('Получены не все доступные объекты.')
	def get(self):
		return requests.post(self.url, json=self.json, headers=self.headers)
	def display(self):
		result = self.get()
		print(json.dumps(dict(result.headers), sort_keys=True, indent=2))
		print(json.dumps(result.json(), ensure_ascii=False, sort_keys=True, indent=2))
if __name__ == '__main__':
	request = request(**{
		'token': os.environ.get('token'),
		'url': 'https://api.direct.yandex.com/json/v5/campaigns',
	})
	#	request.main()
	request.display()
