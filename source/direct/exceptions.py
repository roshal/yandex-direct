
class exception(Exception):
	'''
	yandex direct api exceptions
	'''

class exception_no_data(exception):
	'''
	raised when api result without data key
	'''

class exception_connection_error(exception):
	'''
	raised if http status code is not equal to standard 200
	'''
