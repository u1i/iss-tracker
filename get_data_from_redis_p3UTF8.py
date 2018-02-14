import redis
import json
import datetime
import time

from geopy.geocoders import Nominatim
geolocator = Nominatim()

redis_host = "redis-19233.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
redis_port = 19233
redis_auth = "sotong"

rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
with open('keys.txt') as kfile:
	lines = kfile.read().splitlines()

	print ("Utime, Timestamp, Latitude, Longitude, Location")
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
				location = geolocator.reverse(latlon, language='en')
				break
			except:
				pass

		if location.address == None:
			addr = ""
		else:
			addr = location.address

		timestamp_human = datetime.datetime.fromtimestamp( int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
		print (str(timestamp) + "," + str(timestamp_human) + " UTC," + str(lat) + "," + str(lon) + ',"' + addr + '"')
		# print timestamp, d
