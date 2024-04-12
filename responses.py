import random
from datetime import datetime

import functions


def handle_response(message) -> str:
    p_message = message.lower()
    begin = p_message.split(" ")[0]
    respones = {
        "hello bonnie": "HIIII :3",
        "hi bonnie": "HIIII :3",
        "bye bonnie": "bye bitch :3",
        "danku bonnie": "no problem :3",
        "thx bonnie": "no problem :3",
        "thank you bonnie": "no problem :3",
        ":3": "meow :3",
        "!help": "functions:\n\n "
        "- 'sunset [place] [date] [timezone (gmt+x)]':\n"
        "gives the time of the sunset on a certain place and/or date, "
        "if date isn't specified it uses the current date, if timezone isn't specified it uses gmt \n"
        "example: sunset nepal 20/3/2004 3\n\n"
        "- 'sunrise [place] [date]':\n"
        "gives the time of the sunrise on a certain place and/or date, "
        "if date isn't specified it uses the current date, if timezone isn't specified it uses gmt \n"
        "example: sunrise nepal 20/3/2004 3\n\n"
        "- 'noon [place] [date]':\n"
        "gives the time of the noon on a certain place and/or date, "
        "if date isn't specified it uses the current date, if timezone isn't specified it uses gmt \n"
        "example: noon nepal 20/3/2004 3\n\n"
        "- 'apod [date]': \n"
        "NASA astronomy picture of the day, if the date isn't specified it uses the current date\n"
        "example: apod 20/3/2004\n\n"
        "- '!roll [number]':\n"
        "rolls a dice, if you don't specify a number it rolls a d6\n"
        "example: !roll 1 2\n\n",
    }
    function_astronomy = {"sunset", "sunrise", "noon"}
    if p_message in respones:
        return respones[p_message]
    elif "!roll" in p_message:
        return roll(p_message)
    elif begin in function_astronomy:
        adres, date, zone = get_place_date(p_message)
        result = functions.sunsetrise(address=adres, datum=date, zone=zone, kind=begin)
        hs = int(result)
        ms = int((result - hs) * 60)
        return f"{begin} {hs % 24}:{ms % 60}"
    elif begin == "apod":
        date = get_date(p_message)
        apod = functions.astronomy(datum=date)
        url = apod["hdurl"]
        datum = apod["date"]
        title = apod["title"]
        exp = apod["explanation"]

        return f"{url}\n Date: {datum}\n Title: {title}\n\n Explanation: {exp}"
    elif "love" in p_message and "bonnie" in p_message:
        return "I love you too <3"


def get_place_date(p_message):
    parts = p_message.split(" ")
    if len(parts) == 3:
        day, month, year = parts[2].split("/")
        date = datetime(int(year), int(month), int(day))
        zone = 0
    elif len(parts) == 4:
        day, month, year = parts[2].split("/")
        date = datetime(int(year), int(month), int(day))
        zone = int(parts[3])
    else:
        date, zone = datetime.today(), 0
    place = parts[1]
    return place, date, zone


def get_date(p_message):
    parts = p_message.split(" ")
    if len(parts) == 2:
        day, month, year = parts[1].split("/")
        date = datetime(int(year), int(month), int(day))
    else:
        date = datetime.today()
    return date


def roll(p_message):
    parts = p_message.split(" ")
    i = int(parts[1]) if len(parts) > 1 else 6
    return str(random.randint(a=1, b=i))
