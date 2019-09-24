
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
					'ON',
					'OFF',
				],
			},
			'FieldNames': [
				'Id',
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
			if item['TextCampaign']['BiddingStrategy']['Network']['BiddingStrategyType'] != 'SERVING_OFF':
				items.append(item['Id'])
		offest = json.get('LimitedBy')
		if not offest:
			break
	del json
	del offest
	#
	slices = tuple(items[slice(index, index + 10)] for index in range(0, len(items), 10))
	old = []
	for items in slices:
		request = methods['Bids']['get'].request({
			'SelectionCriteria': {
				'CampaignIds': items,
			},
			'FieldNames': [
				'KeywordId',
				'AdGroupId',
				'CampaignId',
				'ContextBid',
			],
		})
		old.append(request.send().json()['result']['Bids'])
	for items in slices:
		request = methods['Bids']['setAuto'].request({
			'Bids': [{
				'CampaignId': item,
				'ContextCoverage': 1,
				'Scope': [
					'NETWORK',
				],
			} for item in items],
		})
		request.send()
	new = []
	for items in slices:
		request = methods['Bids']['get'].request({
			'SelectionCriteria': {
				'CampaignIds': items,
			},
			'FieldNames': [
				'KeywordId',
				'AdGroupId',
				'CampaignId',
				'ContextBid',
			],
		})
		new.append(request.send().json()['result']['Bids'])
	import operator
	for item in zip(*(item for items in zip(old, new) for item in items)):
		mapping = {key: (item[0][key], item[1][key]) for key in set(item[0]) & set(item[1]) if item[0][key] != item[1][key]}
		if mapping:
			print('-', *(str(item[0][string]).rjust(12) for string in ('CampaignId', 'AdGroupId', 'KeywordId')))
			for key, value in mapping.items():
				print(' ', key, *(str(item).rjust(12) for item in value), operator.truediv(*reversed(value)))
	del operator
	del old
	del new
