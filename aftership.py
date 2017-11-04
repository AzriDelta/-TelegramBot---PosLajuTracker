import aftership

class aftership_track:
	#---------------------start of API poslaju tracker#---------------------

	API_KEY = '1fcd696a-b4b9-4150-baca-6bcadd010a13'

	#get API object
	api = aftership.APIv4(API_KEY) #object constructor
	slug = 'pos-laju' #courier
	#number = 'ER028982330MY' #tracking number for testing purposes

	# gets list of supported couriers
	def get_courier():
		couriers = api.couriers.all.get()
		return couriers
		
	def create_track(number):
		return api.trackings.post(tracking=dict(slug=slug, tracking_number=number, title="Test"))
		#{u'tracking': { ... }}
		
	def get_track(number):
		return api.trackings.get(slug, number, fields=['title', 'created_at'])
		#{u'tracking': { ... }}

	def delete_track(number):
		return api.trackings.delete(slug, number)
		#{u'tracking': { ... }}
		


	#---------------------End of API poslaju tracker#---------------------