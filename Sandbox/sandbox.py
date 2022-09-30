# sandbox to test python code
import datetime
today = datetime.date.today()
today_with_time = datetime.datetime(
    year=today.year, 
    month=today.month,
    day=today.day,
)
print(today_with_time)
print(datetime.datetime(2022, 9, 30) - today_with_time)
print(datetime.datetime(2022, 9, 30) > today_with_time)