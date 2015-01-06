rsa = read.csv('Auckland 2014.csv',stringsAsFactors=FALSE,header=F)
names(rsa) = c('day','dayofweek','month','year','time1','height1','time2','height2'
			,'time3','height3','time4','height4')

dates=as.Date(paste(rsa$year,rsa$month,rsa$day,sep='-'))

rsa = rsa[,-c(1:4)]
rsa$time1 = as.POSIXct(paste(dates,rsa$time1))
rsa$time2 = as.POSIXct(paste(dates,rsa$time2))
rsa$time3 = as.POSIXct(paste(dates,rsa$time3))
rsa$time4 = as.POSIXct(paste(dates,rsa$time4))

# Currently each day has 4 measurements. Want to combine it to a single entry
# for each 
new.tides = data.frame(times=c(rsa$time1,rsa$time2,rsa$time3,rsa$time4),
			heights=c(rsa$height1,rsa$height2,rsa$height3,rsa$height4))

new.tides = new.tides[ order(new.tides$times),]
sample = new.tides[1:(31*4),]
zoo.me = zoo(sample$heights,order.by=sample$times)
zoo.full = zoo(new.tides$heights,order.by=new.tides$times)
plot(zoo.full)

#loess??????

heights = new.tides$heights
average = mean(heights)
