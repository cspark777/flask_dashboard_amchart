import os
import datetime
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, BSpline
import base64
import random

sample_country_list = ['US', 'JP', 'AU', 'CH', 'UK']

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
 	"JP": [-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2
 		],
 	"AU": [-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2
 		],
 	"CH": [-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2
 		],
 	"UK": [-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2,
 		-3, -1, 1, 3, -2, 5, 0, 7, 8, 6, 3, -1, -3, -5, -7, -4, 1, 0, 5, 2
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

#=================  create chart png files by cron job every day =================
basedir = os.path.abspath(os.path.dirname(__file__))
chart_images_path = basedir + "/sampling/static/chart_images/"

def make_chart_thumbnail(country, x, y, date_interval, is_positive):
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    img_file_path_dark = chart_images_path + "/" + country + "_" + today_str + "_" + str(date_interval) + "_dark.png"
    img_file_path_light = chart_images_path + "/" + country + "_" + today_str + "_" + str(date_interval) + "_light.png"

    x1 = np.array(x)
    y1 = np.array(y)    

    #define x as 200 equally spaced values between the min and max of original x 
    xnew = np.linspace(x1.min(), x1.max(), 200) 

    #define spline
    spl = make_interp_spline(x1, y1, k=3)
    y_smooth = spl(xnew)

    #create smooth line chart 
    if is_positive == 1:
        plt.plot(xnew, y_smooth, linewidth=7.0, color="#01e29a")
    else:
        plt.plot(xnew, y_smooth, linewidth=7.0, color="#6a303f")

    plt.axis('off')    
    

    plt.savefig(img_file_path_dark, facecolor="#1d2132", bbox_inches='tight')
    plt.savefig(img_file_path_light, facecolor="#ffffff", bbox_inches='tight')
    
def make_chart_img_for_all_country(date_interval):
    today = datetime.datetime.today()
    data = get_trend_data_list()
    detail_data = get_main_data_list()

    for dt in detail_data:        
        x = []
        y = []
        for i in range(date_interval):
            delta = date_interval - i - 1
            d = today - datetime.timedelta(days=delta)        
            date_step = int(d.timestamp()) * 1000
            
            x.append(date_step)
            y.append(data[dt["country"]][date_interval - i - 1])
        
        if dt["daily_change"] > 0:
            make_chart_thumbnail(dt["country"], x, y, date_interval, 1)
        else:
            make_chart_thumbnail(dt["country"], x, y, date_interval, 0)

def get_chart_img_for_country(country, date_interval, is_dark=1):
    today_str = datetime.datetime.today().strftime('%Y-%m-%d')
    if is_dark==1:
        img_file_path = chart_images_path + country + "_" + today_str + "_" + str(date_interval) + "_dark.png"
    else:
        img_file_path = chart_images_path + country + "_" + today_str + "_" + str(date_interval) + "_light.png"

    encoded = base64.b64encode(open(img_file_path, "rb").read())
    return "data:image/png;base64," + encoded.decode('utf-8')

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

def get_main_data_for_allcountry(date_interval, is_dark=1):
    detail_data_list = get_main_data_list()
    data = []
    for dt in detail_data_list:                
        dt["trend_figure"] = get_chart_img_for_country(dt["country"], date_interval, is_dark)
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