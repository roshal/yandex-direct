if __name__ == '__main__':
	from direct.api import api
	import os
	api = api(**{
		'token': os.environ.get('token'),
		'language': 'ru',
	})
	del os
	service = api.service('Campaigns')
	method = service.method('get')
	request = method.request({
		'SelectionCriteria': {
		},
		'FieldNames': (
			'Id',
		),
	})
	response = request.send()
	response.print()
	#	api(**{
	#		'token': os.environ.get('token'),
	#	}).Campaigns.get.request({
	#		'SelectionCriteria': {
	#		},
	#		'FieldNames': [
	#			'Id',
	#		],
	#	}).send().print()
