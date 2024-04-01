from datetime import datetime

from functions import astronomy

# add the apod you want to save here
apod_list = ["2023-09-07",
             "2023-09-08",
             "2023-09-13",
             "2023-10-13",
             "2023-12-14",
             "2024-01-10",
             "2024-02-06",
             "2024-02-18",
             "2024-03-05"]

# change this to the directory you prefer
directory = "/home/jalog/Documents/ugent/Ba2/Semester 2/Sterrenstelsels/APOD/potential_apods"


def list_to_date(date_string):
    date_format = "%Y-%m-%d"
    datetime_variable = datetime.strptime(date_string, date_format)
    return datetime_variable


for apod in apod_list:
    apod_date = list_to_date(apod)
    astronomy(apod_date, save=directory)
