def run():
	from direct.api import api
	from operator import truediv
	from os import environ
	from random import randint
	from time import gmtime
	from time import sleep
	from time import strftime
	api = api(**{
		'token': environ.get('token'),
		'language': 'ru',
	})
	del environ
	services = {
		'Bids': api.service('Bids'),
		'Campaigns': api.service('Campaigns'),
	}
	del api
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
	while True:
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
				if item['TextCampaign']['BiddingStrategy']['Search']['BiddingStrategyType'] != 'SERVING_OFF':
					items.append(item['Id'])
			offest = json.get('LimitedBy')
			if not offest:
				break
		#	del json
		#	del offest
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
					'Bid',
				],
			})
			old.append(request.send().json()['result']['Bids'])
		for items in slices:
			request = methods['Bids']['setAuto'].request({
				'Bids': [{
					'CampaignId': item,
					'MaxBid': 40 * 10 ** 6,
					#	'Position': 'FOOTERFIRST' if 4 < gmtime().tm_hour < 17 else 'FOOTERBLOCK',
					#	'Position': 'P12',
					'Position': 'PREMIUMBLOCK' if 4 < gmtime().tm_hour < 17 else 'FOOTERFIRST',
					'Scope': [
						'SEARCH',
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
					'Bid',
				],
			})
			response = request.send()
			new.append(response.json()['result']['Bids'])
			print(response.get_json_headers())
		for item in zip(*(item for items in zip(old, new) for item in items)):
			mapping = {key: (item[0][key], item[1][key]) for key in set(item[0]) & set(item[1]) if item[0][key] != item[1][key]}
			if mapping:
				print('-', *(str(item[0][string]).rjust(12) for string in ('CampaignId', 'AdGroupId', 'KeywordId')))
				for key, value in mapping.items():
					print(' ', key, *(str(item).rjust(12) for item in value), truediv(*reversed(value)))
		#	del truediv
		#	del old
		#	del new
		interval = randint(256, 768)
		print(strftime('%y-%m-%d %H:%M:%S'), interval)
		sleep(interval)
if __name__ == '__main__':
	run()
