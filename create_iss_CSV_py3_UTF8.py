import redis
import json
import datetime
import time

from geopy.geocoders import Nominatim
geolocator = Nominatim()

redis_host = "redis-XXXXXX.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
redis_port = 19233
redis_auth = "XXXXX"

rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
with open('keys.txt') as kfile:
	lines = kfile.read().splitlines()


print ("Utime, Timestamp, Latitude, Longitude, TimeAndLocation")
for k in lines:
	d1 = rc.get(k)

	dx = d1.decode("utf-8")

	d2=dx.replace("u'",'"')
	d3=d2.replace("'",'"')
	# data = json.loads(d2.decode("utf-8"))

	data = json.loads(d3)
	timestamp = k[4:]
	lat = data["latitude"]
	lon = data["longitude"]
	latlon = str(lat) + "," + str(lon)

	while True:
		try:
			location = geolocator.reverse(latlon, language='en', timeout=10)
			break
		except Exception as e:
			# pass
			print("GEOPY_RECONNECT_SLEEP10SECONDS: ",latlon,e)
			time.sleep(10)

	if location.address == None:
		addr = ""
	else:
		addr = location.address
#		print (latlon)
#		print (addr)

	# timestamp_human = datetime.datetime.fromtimestamp( int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
	timestamp_human = datetime.datetime.fromtimestamp( int(timestamp)).strftime('%H:%M:%S')

	timeandloc = str(timestamp_human) + " " + addr
	# print (str(timestamp) + "," + str(timestamp_human) + " UTC," + str(lat) + "," + str(lon) + ',"' +  '"')
	print (str(timestamp) + "," + str(timestamp_human) + " UTC," + str(lat) + "," + str(lon) + ',"' + timeandloc + '"')

