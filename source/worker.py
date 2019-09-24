
from operator   import truediv  as p__truediv
from os         import environ  as p__environ
from random     import randint  as p__randint
from time       import gmtime   as p__gmtime
from time       import sleep    as p__sleep
from time       import strftime as p__strftime

from direct.api import api      as p__api


def worker():
	api = p__api(**{
		'token': p__environ.get('token'),
		'language': 'ru',
	})
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
		##	del json
		##	del offest
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
					##	'MaxBid': 40 * 10 ** 6,
					##	'Position': 'FOOTERFIRST' if 4 < p__gmtime().tm_hour < 17 else 'FOOTERBLOCK',
					##	'Position': 'P12',
					'Position': 'PREMIUMBLOCK' if 4 < p__gmtime().tm_hour < 17 else 'FOOTERFIRST',
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
					print(' ', key, *(str(item).rjust(12) for item in value), p__truediv(*reversed(value)))
		##	del p__truediv
		##	del old
		##	del new
		interval = p__randint(256, 768)
		datetime = p__strftime('%y-%m-%d %H:%M:%S')
		print('close', datetime, interval)
		p__sleep(interval)


if __name__ == '__main__':
	datetime = p__strftime('%y-%m-%d %H:%M:%S')
	print('start', datetime)
	worker()
