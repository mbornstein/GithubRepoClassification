
def url_to_full_name(url):
	tokens = url.split('/')
	return tokens[-2] + '/' + tokens[-1]
