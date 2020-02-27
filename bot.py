import os
import requests
import json
import time
import math
import datetime

portfolio = {
	'cash':10000,
	'stocks':{}
}

movers_url = "https://api.tdameritrade.com/v1/marketdata/$DJI/movers"
hours_url = "https://api.tdameritrade.com/v1/marketdata/EQUITY/hours"

hours_text = requests.get(hours_url, {
		'apikey':'W2PW3SRFYIYOSFWV0VCG5UNPI5ZXEYUT',
		'date': datetime.date.today().isoformat()
		}).text

hours = json.loads(hours_text)
curtime = datetime.date.today()

if(hours.get('equity').get('EQ').get('isOpen') == True):
	trade()
else:
	print("Markets are currently closed")

def trade():
	while(True):
		item_text = requests.get(movers_url, {
        		'apikey':'W2PW3SRFYIYOSFWV0VCG5UNPI5ZXEYUT'
		}).text

		items = json.loads(item_text)
		max_item = None
		for item in items:
			if(max_item == None and item['direction'] == 'up'):
				max_item = item
			elif(max_item != None and max_item.get('change') < item['change'] and item['direction'] == 'up'):
				max_item = item

		if(max_item == None):
			print("No good stocks to buy!")
		else:
			max_amount = math.floor(portfolio['cash'] / max_item['last'])
			if(max_amount < 1):
				print("Out of cash")
			else:
				portfolio['stocks'][max_item['symbol']] = {'amount': max_amount, 'cost': max_amount*max_item['last']}
				portfolio['cash'] -= max_amount*max_item['last']



		print(portfolio)
		time.sleep(10)


def getTime(timestr):
	ret_str = ''
	f = False
	for c in timestr:
		if(f == False and c == 'T'):
			f = True
		if(f == True and c != 'T'):
			ret_str += c
		if(f == True and c == '-'):
			return ret_str
