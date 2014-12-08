#import urllib2
#import StringIO

#rb_socket = urllib2.urlopen('http://www.rbnz.govt.nz/statistics/key_graphs/graphdata.xls')
#rb_socket = rb_socket.read()
#rb_buffer = StringIO.StringIO(rb_socket)
#data = pd.io.excel.read_excel(rb_buffer, 7, skiprows=2,index_col=2)


import pandas as pd
import re

df = pd.read_csv("graphdata.csv")

# Grabs the dates
dates = df['DATE']

# Replaces 'M' with '-' and makes a date object out of it
new_dates = pd.DataFrame(map(lambda x: re.sub("M","-",x), dates))
new_dates = pd.DatetimeIndex(new_dates[0]).to_period('M')

df = pd.DataFrame(df['R$USD'],index=new_dates)

