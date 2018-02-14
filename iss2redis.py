import redis
import requests
import json

url = "http://api.open-notify.org/iss-now.json"
redis_host = "redis-XXXX.c1.ap-southeast-1-1.ec2.cloud.redislabs.com"
redis_port = 19233
redis_auth = "MYPASSWORD"

def iss_do():
	iss = requests.get(url)
	
	iss_data = json.loads(iss.text)
	
	iss_timestamp = iss_data["timestamp"]
	iss_location = iss_data["iss_position"]

        # Open Redis Connection
	rc = redis.StrictRedis(host=redis_host, port=redis_port, db=0, password=redis_auth)

        # Write current ISS Position to Redis
	key_name = "ISS-" + str(iss_timestamp)
	rc.set(key_name, str(iss_location))

        return str(iss_location)
	
	
