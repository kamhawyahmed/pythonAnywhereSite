import datetime as dt
print(dt.datetime.now().strftime('%B %d, %Y'))
print(dt.datetime.now().timestamp())
now = int(dt.datetime.now().timestamp())
print(now, dt.datetime.fromtimestamp(now))