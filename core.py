#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import requests
import json
import logging

#logging.basicConfig(level="DEBUG", format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s')

params = (
    ('book', 'eth_cad'),
)

try:
	r_quad = requests.get('https://api.quadrigacx.com/v2/ticker', params=params)
	r_quad_dict = json.loads(r_quad.text)
	quadriga_last = r_quad_dict["last"]
except:
	quadriga_last = 0

try:
	r_gdax = requests.get('https://api.gdax.com/products/ETH-USD/ticker')
	r_gdax_dict = json.loads(r_gdax.text)
	gdax_price = round(float(r_gdax_dict["price"]), 2)
except:
	gdax_price = 0

try:
	r_korbit = requests.get('https://api.korbit.co.kr/v1/ticker?currency_pair=eth_krw')
	r_korbit_dict = json.loads(r_korbit.text)
	korbit_price = r_korbit_dict["last"]
	logging.debug(r_korbit.text)
	logging.debug("Korbit price: %s" % korbit_price)
except:
	korbit_price = 0

currFrom = "CAD"
currTo = ["USD", "KRW"]

urlParamTo = currTo[0]
if len(currTo) > 1:
    urlParamTo = ",".join(currTo)

url = "http://api.fixer.io/latest?base=" + currFrom + "&symbols=" + urlParamTo
r_fixer = requests.get(url)
r_fixer_dict = json.loads(r_fixer.text)
cad_usd_rate = r_fixer_dict["rates"]['USD']
cad_krw_rate = r_fixer_dict["rates"]['KRW']
logging.debug("cadusd %s, cadkrw %s" % (cad_usd_rate, cad_krw_rate))

quadriga_to_usd = float(quadriga_last) * float(cad_usd_rate)
gdax_to_cad = float(gdax_price) / float(cad_usd_rate)
quadriga_to_krw = float(quadriga_last) * float(cad_krw_rate)
logging.debug("%s %s" % (float(quadriga_last), float(cad_krw_rate)))
logging.debug("quadriga_to_krw %s" % quadriga_to_krw)
korbit_to_cad = float(korbit_price) / float(cad_krw_rate)
logging.debug("korbit price %s, cadkrw %s" % (float(korbit_price), float(cad_krw_rate)))

# Calculate percentage difference
x = float(quadriga_last) - gdax_to_cad
diff_gdax = x / float(quadriga_last) * 100

y = float(quadriga_last) - korbit_to_cad
diff_korbit = y / float(quadriga_last) * 100

# in menu bar
print("$%s" % quadriga_last)

# in submenu
print("---")
print("$%s Quadriga CAD" % quadriga_last)
print("$%s GDAX CAD" % round(gdax_to_cad, 2))
print("$%s Korbit CAD" % round(korbit_to_cad, 2))
print("---")
print("$%s Quadriga USD" % round(quadriga_to_usd,2))
print("$%s GDAX USD" % round(gdax_price, 2))
print("---")
print("₩%s Quadriga" % format(int(quadriga_to_krw), ",d"))
print("₩%s Korbit" % format(int(korbit_price), ",d"))
print("---")
print("Q Diff GDAX: %s%%" % round(diff_gdax, 1))
print("Q Diff Korbit: %s%%" % round(diff_korbit, 1))
print("---")
print("Links:")
print("Quadriga Trade | href=https://www.quadrigacx.com/trade")
print("GDAX ETH-USD | href=https://www.gdax.com/trade/ETH-USD")
print("Korbit ETH Market | href=https://www.korbit.co.kr/eth_market")