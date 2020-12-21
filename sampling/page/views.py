from flask import render_template, url_for, flash, request, send_file, redirect, Blueprint, jsonify
from flask_login import current_user, login_required

import random
import string
import os, sys
from collections import deque
import settings

import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline

import calendar
from datetime import timezone 
import datetime
import time
import json
import base64

from data import *

basedir = os.path.abspath(os.path.dirname(__file__))
page = Blueprint('page', __name__)

def log_message(message):
    print(message)
    '''
    hs = open("web_log.txt","a", encoding="utf8")
    hs.write(message + "\n")
    hs.close() 
    '''

'''
day_interval : 90, 180, 360
country_filter=> 0: all, 1: G10, 2: EM
'''
def get_mainpage_data(date_interval, country_filter):
    
    chart_data = {}
    chart_data["world_chart_data"] = get_world_chart_data()
    chart_data["country_data"] = get_main_data_for_allcountry(date_interval, country_filter)
    return chart_data

@page.route('/', methods=['GET', 'POST'])
def index():     
    chart_data = get_mainpage_data(90, 0) 
    chart_data = json.dumps(chart_data) 
    return render_template('index.html', chart_data=chart_data)

@page.route('/get_mainpage', methods=['POST'])
def get_mainpage():
    date_interval = int(request.form.get("date_interval"))
    country_filter = int(request.form.get('country_filter'))
    chart_data = get_mainpage_data(date_interval, country_filter) 
    chart_data = json.dumps(chart_data) 
    return jsonify(chart_data)

@page.route('/detail/<country>', methods=['GET', 'POST'])
def get_detail(country):
    if request.method == 'GET':
        chart_data = get_detail_data_for_country(country, 90)
        chart_data = json.dumps(chart_data) 
        return render_template('detail.html', chart_data=chart_data)        
    else:
        date_interval = request.form.get('date_interval')
        chart_data = get_detail_data_for_country(country, int(date_interval))
        chart_data = json.dumps(chart_data) 
        return jsonify(chart_data)

