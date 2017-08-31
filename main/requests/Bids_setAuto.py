if __name__ == '__main__':
	from direct.api import api
	import os
	api = api(**{
		'token': os.environ.get('token'),
		'language': 'ru',
	})
	service = api.service('Bids')
	method = service.method('setAuto')
	request = method.request({
		'Bids': [{
			'CampaignId' : item,
			'Position' : 'PREMIUMBLOCK',
			'CalculateBy' : 'DIFF',
			'IncreasePercent' : 50,
			'Scope' : [
				'SEARCH',
			],
		} for item in [
			232659,
			232660,
			232661,
		]],
	})
	response = request.send()
	print(response.get_json_json())
