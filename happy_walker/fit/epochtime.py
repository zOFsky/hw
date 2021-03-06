import time, datetime

second = 1000
hour = second * 3600
day = hour * 24
week = day * 7
month = day * 30
year = day * 365

def date_to_epoch():
    now = datetime.datetime.now()
    format = '%Y-%m-%d'
    date = f'{now.year}-{now.month}-{now.day}'
    return(time.mktime(time.strptime(date, format)))

def epoch_to_date(time_milis):
    return time.strftime('%Y-%m-%d', time.localtime(time_milis/1000))

def extract_hour(time_milis):
    return time.strftime('%H:%M', time.localtime(time_milis/1000))