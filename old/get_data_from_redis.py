import redis
import json
import datetime
import time

redis_host = "redis-XXXX.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
redis_port = 19233
redis_auth = "MYPASSWORD"

rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)
with open('keys.txt') as kfile:
	lines = kfile.read().splitlines()

	for k in lines:
		d1 = rc.get(k)
		d2 = d1.replace("u'",'"')
		d3 = d2.replace("'",'"')

		data = json.loads(d3)
		timestamp = k[4:]
		lat = data["latitude"]
		lon = data["longitude"]
		timestamp_human = datetime.datetime.fromtimestamp( int(timestamp)).strftime('%Y-%m-%d %H:%M:%S')
		print str(timestamp_human) + "," + str(lat) + "," + str(lon)
		# print timestamp, d
