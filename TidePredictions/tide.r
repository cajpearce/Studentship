library(zoo)


places = c('Auckland','Port Taranaki','Westport','Bluff')

place = paste(places[4],'2014.csv')

# read in the CSV for a place
rsa = read.csv(place,stringsAsFactors=FALSE,header=F)

# rename the headers (not stored in the CSV)
names(rsa) = c('day','dayofweek','month','year','time1','height1','time2','height2'
			,'time3','height3','time4','height4')

# creates dates from the date data stored in the CSV
dates=as.Date(paste(rsa$year,rsa$month,rsa$day,sep='-'))

# Remove previous date storage methods
rsa = rsa[,-c(1:4)]

# creates date-times for each time slot
rsa$time1 = as.POSIXct(paste(dates,rsa$time1))
rsa$time2 = as.POSIXct(paste(dates,rsa$time2))
rsa$time3 = as.POSIXct(paste(dates,rsa$time3))
rsa$time4 = as.POSIXct(paste(dates,rsa$time4))

# Currently each day has 4 measurements. Want to combine it to a single entry
new.tides = data.frame(times=c(rsa$time1,rsa$time2,rsa$time3,rsa$time4),
			heights=c(rsa$height1,rsa$height2,rsa$height3,rsa$height4))

# order it to make sure that the entries are sequential
new.tides = new.tides[ order(new.tides$times),]
new.tides = as.data.frame(new.tides)

# remove NA values
new.tides = new.tides[-which(is.na(new.tides$heights)),]

# Create a zoo
zoo.full = zoo(new.tides$heights,order.by=new.tides$times)


# Start plotting
pdf("Rplots.pdf",width=8,height=5)
plot(zoo.full,type="l",col="grey")


my.heights = new.tides$heights

# get the average (middle point) height
middle = mean(my.heights,na.rm=TRUE)

# split the dataset into two parts - those above (high tide) and those below
# (low tide). The split being the middle (average calculated above)
above = new.tides[which(my.heights > middle),]
below = new.tides[which(my.heights <= middle),]

# draws a red line for high tide
lines(above$times,above$heights,col="red",lwd=2)

# draws a blue line for low tide
lines(below$times,below$heights,col="blue",lwd=2)


# Manually obtained new moon dates (NZ) from the internet. Wanted to see if they
# coincided with any spikes - there is some evidence. Perhaps Seasonal data has 
moon.dates = as.POSIXct(c("2014-01-02","2014-01-31","2014-03-01","2014-03-31","2014-04-29",
		"2014-05-29","2014-06-27","2014-07-27","2014-08-26","2014-09-24",
		"2014-10-24","2014-11-23","2014-12-22"))

# month data...
months = as.POSIXct(paste("2014",1:12,"01",sep="-"))

abline(v=moon.dates,lwd=1,lty="dashed",col="darkgreen")
#abline(v=months)
abline(h=middle)
dev.off()
