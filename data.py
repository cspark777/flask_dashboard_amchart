import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import base64
import random

sample_country_list = ['US', 'JP', 'AU', 'CH', 'UK']
sample_G10_country_list = ['US', 'JP', 'UK']
sample_EM_country_list = ['AU', 'CH']


sample_world_chart_data = [
    {"id":'US', "value": 5.5},
    {"id":'JP', "value": -2.1},
    {"id":'CA', "value": 3.5},
    {"id":'ID', "value": 7.5},
    {"id":'AU', "value": 1.5},
    {"id":'BR', "value": -5.5},
    {"id":'CO', "value": -7.5},
    {"id":'VE', "value": 2.5},
    {"id":'PH', "value": 6.5}
]

sample_main_data_list = [
    {"country": "US", "pulse_score": 7.1, "30day_change": 1.23, "fx_price": 99.10, "daily_change": 1.2},
    {"country": "JP", "pulse_score": 0, "30day_change": 0.05, "fx_price": 100.2, "daily_change": 1.6},
    {"country": "AU", "pulse_score": 3.23, "30day_change": 3.18, "fx_price": 0.72, "daily_change": -0.5},
    {"country": "CH", "pulse_score": 8.05, "30day_change": -2.21, "fx_price": 6.72, "daily_change": 3},
    {"country": "UK", "pulse_score": -3.98, "30day_change": 1, "fx_price": 1.27, "daily_change": 0} 
]

sample_trend_data_list_180days = {
	
	"US": [-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2
 		],
 	"JP": [-2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
 		-2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
        -2, -1, 1, 5, 7, 8, 8, 9, 5, 6, 8, 4, 3, -1, -2, -2, -4, -5, -7, -4,
 		],
 	"AU": [7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
 		7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
        7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
        7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
        7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
        7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
        7, 7, 6, 5, 7, 8, 6, 4, 2, 0, -1, -1, -3, -5, -1, 1, 2, 4, 5, 6,
 		],
 	"CH": [0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
 		0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
        0, 1, -1, 0, 3, 5, 7, 9, 7, 6, 3, 0, -1, -3, -5, -3, -2, 0, 1, 2,
 		],
 	"UK": [-7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
 		-7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
        -7, -6, -5, -2, 0, 1, 0, 4, 6, 6, 8, 6, 3, 5, 1, -1, -3, -5, -6, -6,
 		],
	
}

#status 1: positive, 0: steady, -1: negative
sample_detail_data = {
    "country": "US", "country_name": "United State of America", "survey": 3.2, "growth": 25.4, "emplovment": 4.3, "inflation": 27.1,
    "housing": 2.3, "current_reading": 78, "prev_reading": 55, "status": 1, 
    "data_detail": [
        {"pulse_detail": "GDP yoy", "sector": "Growth", "current_reading": 1, 
        "prev_reading": 0.9, "trend": 1, "status": 1},
        {"pulse_detail": "Unemployment Rate", "sector": "Employment", "current_reading": 5.6, 
        "prev_reading": 5.6, "trend": 0, "status": 0},
        {"pulse_detail": "Retail Sales", "sector": "Growth", "current_reading": 1.6, 
        "prev_reading": 1.5, "trend": 1, "status": 1},
        {"pulse_detail": "House Price", "sector": "Housing", "current_reading": 120, 
        "prev_reading": 110, "trend": 1, "status": -1},
    ]
}

#================= get calculated data functions =================================

def get_main_data_list():
    return sample_main_data_list

def get_trend_data_list():
    return sample_trend_data_list_180days

def get_country_list():
    return sample_country_list

def get_world_chart_data_list():
    return sample_world_chart_data

def get_detail_data(country, date_interval):
    return sample_detail_data

def check_country_by_filter(country_name, country_filter):
    if country_filter == 0 and country_name in sample_country_list:
        return True
    if country_filter == 1 and country_name in sample_G10_country_list:
        return True
    if country_filter == 2 and country_name in sample_EM_country_list:
        return True
    return False

#=================

def get_trend_data_for_country(country, date_interval):
    x = []
    y = []

    today = datetime.datetime.today()
    data = get_trend_data_list()

    for i in range(date_interval):
        delta = date_interval - i - 1
        d = today - datetime.timedelta(days=delta)    
        d_str = d.strftime("%Y-%m-%d")
                
        x.append(d_str)
        y.append(data[country][date_interval - i - 1])

    data = {"x": x, "y": y}

    return data

def get_main_data_for_allcountry(date_interval=90, country_filter=0):
    detail_data_list = get_main_data_list()
    data = []
    
    for dt in detail_data_list:                
        if check_country_by_filter(dt["country"], country_filter):
            dt["trend"] = get_trend_data_for_country(dt["country"], date_interval)
            data.append(dt)
    
    return data

def get_world_chart_data():
    world_chart_data = get_world_chart_data_list()

    for w in world_chart_data:
        w["value"] = random.random() * 20 - 10

    return world_chart_data

def get_detail_data_for_country(country, date_interval=90):  
    detail_data = get_detail_data(country, date_interval)  
    trend_data = get_trend_data_for_country(country, date_interval)

    detail_data["trend"] = trend_data
    return detail_data