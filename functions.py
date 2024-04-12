import calendar
import os
import urllib.parse
import urllib.request
from datetime import datetime
from math import sin, cos, tan, asin, acos, pi, radians

import nasapy
import requests


def sunsetrise(address, datum=None, zone=None, kind="sunrise"):
    # url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) + '?format=json' old api
    # url = 'https://nominatim.openstreetmap.org/search?q={}'.format(urllib.parse.quote(address))
    url = "https://nominatim.openstreetmap.org/search"
    print(url)
    params = {"q": address, "format": "json"}
    response = requests.get(url, params=params)
    response = response.json()
    print(response)
    lat = float(response[0]["lat"])
    long = float(response[0]["lon"])

    if not zone:
        zone = (datetime.now() - datetime.utcnow()).seconds / 3600
    if not datum:
        datum = datetime.today()
    day_of_year = datum.timetuple().tm_yday
    if calendar.isleap(datum.year):
        fracy = (2 * pi / 366) * day_of_year
    else:
        fracy = (2 * pi / 365) * day_of_year
    dates = [
        datetime(datum.year, month=3, day=20),
        datetime(datum.year, month=6, day=21),
        datetime(datum.year, month=10, day=22),
        datetime(datum.year, month=12, day=21),
    ]
    map(lambda d: abs(d - datum), dates)
    eqtime = 229.18 * (
        0.000075
        + 0.001868 * cos(fracy)
        - 0.032077 * sin(fracy)
        - 0.014615 * cos(2 * fracy)
        - 0.040849 * sin(2 * fracy)
    )
    date2lengt = {
        datetime(datum.year, month=3, day=20): 0,
        datetime(datum.year, month=6, day=21): pi / 2,
        datetime(datum.year, month=10, day=22): pi,
        datetime(datum.year, month=12, day=21): 3 * pi / 2,
    }
    lengt = date2lengt[dates[0]] + 2 * pi * (datum - dates[0]).days / 356.256
    decl = asin(sin(lengt) * sin(0.40889888214))
    ha = acos(-tan(radians(lat)) * tan(decl)) * 12 / pi
    if kind == "sunrise":
        result = -ha + 12 - eqtime / 60 - long / 15 + zone
    elif kind == "noon":
        result = 12 - eqtime / 60 - long / 15 + zone
    elif kind == "sunset":
        result = ha + 12 - eqtime / 60 - long / 15 + zone
    return result


# config = configparser.ConfigParser()
# config.read('config.ini')
# nasa_key = config['credentials']['nasa_api_key']
nasa_key = os.getenv("nasa_api_key")
nasa = nasapy.Nasa(key=nasa_key)


def astronomy(datum=None, save=False):
    if not datum:
        datum = datetime.today()
    apod = nasa.picture_of_the_day(date=datum, hd=True)
    if apod["media_type"] == "image" and save:
        if "hdurl" in apod.keys():
            title = (
                apod["title"].replace(" ", "_").replace(":", "_")
                + "_"
                + datum.strftime("%d-%m-%Y")
                + ".jpg"
            )
            if isinstance(save, str):
                image_dir = save
            else:
                image_dir = "apod"
            dir_res = os.path.exists(image_dir)
            if not dir_res:
                # os.makedirs(image_dir)
                print("Wrong directory :/")
            else:
                print("Directory okay :3")
            urllib.request.urlretrieve(
                url=apod["hdurl"], filename=os.path.join(image_dir, title)
            )
            print(f"Image saved: {os.path.join(image_dir, title)}")
    return apod
