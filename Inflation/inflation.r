library(gdata)
library(zoo)

df = read.xls("http://www.rbnz.govt.nz/statistics/key_graphs/graphdata.xls",
		sheet = 8, header = TRUE,skip=2,row.names=2)

yearly = gsub("M.*$","",rownames(df))
monthly = gsub("^.*M","",rownames(df))
monthly = sprintf("%02s", monthly)

new.dates = as.yearmon(paste(yearly,monthly,sep="-"))
rownames(df) = new.dates

df$Year = format(new.dates, "%Y")
df$Date = new.dates
