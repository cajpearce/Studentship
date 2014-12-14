#import urllib2
#import StringIO
import pandas as pd
import urllib2
import re


rb_socket = urllib2.urlopen('http://www.rbnz.govt.nz/statistics/key_graphs/graphdata.xls')
data = pd.io.excel.read_excel(rb_socket, 7, skiprows=4)

#df = pd.read_csv("/home/cpea714/Studentship/PyFlation/graphdata.csv")

# Grabs the dates
dates = data['DATE']

# Replaces 'M' with '-' and makes a date object out of it
new_dates = pd.DataFrame(map(lambda x: re.sub("M","-",x), dates))
new_dates = pd.DatetimeIndex(new_dates[0]).to_period('M')

df = pd.DataFrame(data['R$USD'],index=new_dates)

