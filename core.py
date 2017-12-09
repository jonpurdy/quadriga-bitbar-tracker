#!/usr/local/bin/python3
# -*- coding: UTF-8 -*-

import requests
import json
import logging
import time

import requests
import pymysql

import config_loader

logging.basicConfig(level="DEBUG", format='[%(asctime)s][%(levelname)s][%(name)s] %(message)s', filename="arbcalc.log")
logging.getLogger('urllib3').setLevel(logging.CRITICAL)

from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!'

def main():


    # Set configuration and logging up first
    config_location = "~/.arb-calc"
    config = config_loader.load_config(config_location)

    DB_IP = config.get('main', 'DB_IP')
    DB_USERNAME = config.get('main', 'DB_USERNAME')
    DB_PASSWORD = config.get('main', 'DB_PASSWORD')

    crypto_list = ['btc', 'eth', 'xrp']


    a = {'name': 'korbit'}
    b = {'name': 'kraken'}
    e_list = [a, b] # used to iterate through db queries

    try:
        db = pymysql.connect(DB_IP, DB_USERNAME, DB_PASSWORD, cursorclass=pymysql.cursors.DictCursor)
    except Exception as e:
        print(e)
        print("Couldn't connect to DB.")
        exit()


    for e in e_list:
        #print("exchange: %s" % e['name'])

        for c in crypto_list:
            #print("crypto: %s" % c)
            
            query = """
            SELECT id, created, exchange, price_usd 
            FROM crypto_historical.%s
            WHERE exchange = '%s'
            ORDER BY created DESC
            LIMIT 1
            """ % (c, e['name'])

            cursor = db.cursor()
            cursor.execute(query)
            result = cursor.fetchall()

            # sets the price of the cryptocurrency for the particular exchange
            # scroll up to see loop-defined variables e and c
            e[c] = result[0]['price_usd']

            # .strftime('%Y-%m-%d %H:%M:%S')

        #print("-----")

    db.close()

    # korbit_prices_usd_dict = {'name': 'korbit', 'btc': float(15000), 'eth': float(440), 'xrp': float(0.24)}
    # kraken_prices_usd_dict = {'name': 'kraken', 'btc': float(14000), 'eth': float(430), 'xrp': float(0.26)}

    # Calculate percentage difference for each pair
    for curr in crypto_list:
        get_price_spread(curr, a[curr], b[curr])



def get_price_spread(curr, a, b):

    # a / b = difference, * 100 = percentage difference
    # a is 150% more/less than b

    print("currency: %s" % curr)
    print("a: $%s" %a)
    print("b: $%s" %b)
    spread = a / b * 100 - 100
    spread = format(float(spread), '.2f')
    print("spread: %s%%" %spread)
    print("----")

def load_config(config_location):
    '''
    Loads config from config.
    '''

    # Getting configuration first
    file_path = os.path.expanduser(config_location)
    # configparser silently fails if the file doesn't exist
    if os.path.isfile(file_path):
        config = configparser.ConfigParser()
        try:
            config.read(file_path)
        except Exception as e:
            print(e)
            print("Couldn't read configuration file.")
    else:
        print("Couldn't open config file. Has it been created as %s ?"
              % config_location)
        return 0

    return config


if __name__ == '__main__':
    main()