#!/usr/bin/python
import json
import os
import time
import sys

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

#{"devices": [
#    { 
#        "type": "probe_type", 
#        "time": 0, 
#        "id": "28-xxxxxxxxxxxx",
#        "value": num, 
#        "location": "str"}]}

dev_path = '/sys/bus/w1/devices/'
start_time = time.time()

def temp_raw(temp_sensor):
	f = open(temp_sensor, 'r')
	lines = f.readlines()
	f.close()
	return lines

def read_temp(temp_sensor):
	lines = temp_raw(temp_sensor)
	while lines[0].strip()[-3:] != 'YES':
		time.sleep(0.2)
		lines = temp_raw(temp_sensor)
	temp_output = lines[1].find('t=')
	if temp_output != -1:
		temp_string = lines[1].strip()[temp_output+2:]
		temp_c = float(temp_string) / 1000.0
		temp_f = temp_c * 9.0 / 5.0 + 32.0
		return temp_f

with open('data.json', 'r') as f: 
	data = json.load(f)

while True:
	tm = "%03d" % (float(time.time() - start_time)/60.0)
	sys.stdout.write("time: %s min " % tm)
	for x in data['devices']:
		str = dev_path + x['id'] + '/w1_slave'
		if os.path.exists(str):
			#print ("%s: %s   " % (x['location'], round(float(read_temp(str)),1)), end="", flush=True)
			sys.stdout.write("%s: %s   " % (x['location'], round(float(read_temp(str)),1)))
		else:
			sys.stdout.write("%s: %s   " % (x['location'], '?'))
	sys.stdout.write("\n")
	time.sleep(60)
