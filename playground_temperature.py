from services.dataset_services import mean_temp_by_month
import pandas as pd
import numpy as np
from datetime import datetime
from services import month_to_date
from services import from_count
from services import to_count
import matplotlib.pyplot as plt


months = mean_temp_by_month(pd.read_csv('services/datasets/weather.csv'))
station_dataset = pd.read_csv('services/datasets/station_cleaned.csv')
popularity_dict = {}
date_list = []

for date in months:
    month = datetime.strptime(date, "%m/%Y").month
    year = datetime.strptime(date, "%m/%Y").year
    dataset = month_to_date(pd.read_csv('services/datasets/trip_cleaned.csv'), month, year)
    date_new = datetime.strptime(date, "%m/%Y")
    date_little = date_new.strftime("%m/%y")
    date_list.append(str(date_little) + "\n %.2f" % months[date])
    for row in range(len(station_dataset)):
        station = station_dataset.loc[row, "station_id"]
        popularity_from = from_count(dataset, station)
        popularity_to = to_count(dataset, station)
        popularity = popularity_from + popularity_to
        if station not in popularity_dict:
            popularity_dict[station] = [popularity]
        else:
            popularity_dict[station].append(popularity)
plt.style.use('seaborn-dark')
for station in popularity_dict:
    plt.plot(date_list, popularity_dict[station], label=station)
plt.xticks(np.arange(0, len(popularity_dict[station]), step=2))
plt.title("Popularity by month (and temperature) for each station")
plt.legend()
plt.show()
print("Mean temperature by month:")
print(months)
indexes = list(popularity_dict)
for station in range(4):
    print("\nPopularity of %s by month: " % indexes[station])
    print(popularity_dict[indexes[station]])

