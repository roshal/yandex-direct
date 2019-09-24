
if __name__ == '__main__':
	#
	from direct.api import api
	#
	import os
	api = api(**{
		'token': os.environ.get('token'),
		'language': 'ru',
	})
	del os
	#
	services = {
		'Bids': api.service('Bids'),
		'Campaigns': api.service('Campaigns'),
	}
	methods = {
		'Campaigns': {
			'get': services['Campaigns'].method('get'),
		},
		'Bids': {
			'get': services['Bids'].method('get'),
			'set': services['Bids'].method('set'),
			'setAuto': services['Bids'].method('setAuto'),
		},
	}
	items = []
	#
	json = {}
	offest = 0
	while True:
		structure = {
			'SelectionCriteria': {
				'Types': [
					'TEXT_CAMPAIGN',
				],
				'States': [
					# 'SUSPENDED',
					'ON',
					'OFF',
				],
			},
			'FieldNames': [
				'Id',
				#	'Name',
				#	'State',
				#	'Status',
				#	'Type',
			],
			'TextCampaignFieldNames': [
				'BiddingStrategy',
			],
		}
		if offest:
			structure['Page'] = {
				'Offset': offest,
			}
		request = methods['Campaigns']['get'].request(structure)
		response = request.send()
		json = response.json()
		for item in json['result']['Campaigns']:
			items.append({
				'id': item['Id'],
				'type': 'search' if item['TextCampaign']['BiddingStrategy']['Network']['BiddingStrategyType'] == 'SERVING_OFF' else 'network' if item['TextCampaign']['BiddingStrategy']['Search']['BiddingStrategyType'] == 'SERVING_OFF' else 'common',
			})
		offest = json.get('LimitedBy')
		if not offest:
			break
	del json
	del offest
	#
	def diff(a, b):
		return {key: (a[key], b[key]) for key in set(a) & set(b) if a[key] != b[key]}
	#
	for items in [items[slice(index, index + 10)] for index in range(0, len(items), 10)]:
		sequence = []
		request = methods['Bids']['get'].request({
			'SelectionCriteria': {
				'CampaignIds': [item['id'] for item in items],
			},
			'FieldNames': [
				'KeywordId',
				'AdGroupId',
				'CampaignId',
				'MinSearchPrice',
				'ContextCoverage',
				'Bid',
			],
		})
		print(request.send().get_json_body())
		sequence.append(request.send().json()['result']['Bids'])
		methods['Bids']['setAuto'].request({
			'Bids': [{
				'CampaignId': item['id'],
				'Position': 'PREMIUMBLOCK',
				'CalculateBy': 'DIFF',
				'IncreasePercent': 50,
				'Scope': [
					'SEARCH',
				],
			} for item in items if item['type'] is 'search'],
		}).send()
		methods['Bids']['set'].request({
			'Bids': [{
				'KeywordId': item['id'],
				'ContextBid': item['bid'] / 2,
			} for item in items if item['type'] is 'search'],
		}).send()
		sequence.append(request.send().json()['result']['Bids'])
		for item in zip(*sequence):
			differences = diff(*item)
			if differences:
				print(item[0]['CampaignId'], item[0]['AdGroupId'], item[0]['KeywordId'])
				for key, value in differences.items():
					print(' ', key, *map(lambda value: str(value).rjust(12), value))
