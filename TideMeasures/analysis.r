################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################
library(zoo)
z1 = zoo (new.first.set$height, new.first.set$datetime)
z2 = zoo (new.second.set$height, new.second.set$datetime)

m = merge(z1, z2)

t1 = ts(new.first.set$height, start = as.numeric(new.first.set$datetime[1]),
	end = as.numeric(new.first.set$datetime[length(new.first.set$datetime)]),
	frequency = 60)

library(TSA)
periodogram(t1)

#plot(m)

# try to figure out the max height
get.extreme.tides = function(tide.set) {
	# TODO: include functionality for testing to make sure that the ends of 
	# the dataset don't reference high/low tides


	#reference
	ht = tide.set$height
	dt = tide.set$datetime

	# rough middle point
	middle = mean(ht)

	# to store dates
	all.extremes = numeric(0)

	# are we currently above middle
	above.middle = ht[1] > middle
	
	# what are our current extremes
	curr.extreme = ht[1]
	curr.extreme.date = dt[1]

	for (i in 2:length(dt)) {
		curr = ht[i]

		if ((curr > middle & !above.middle) | (curr < middle & above.middle)) {
			# at the switch, reset everything
			
			# need this logic block to make sure the vector is of
			# the form POSIXct, not numeric
			if (length(all.extremes) == 0) {
				all.extremes = curr.extreme.date
			} else {
				all.extremes[length(all.extremes) + 1] = curr.extreme.date
			}
			curr.extreme.date = dt[i]
			curr.extreme = curr
			above.middle = curr > middle
		}
		if ((above.middle & curr > curr.extreme) | (!above.middle & curr < curr.extreme)) {
			curr.extreme = curr
			curr.extreme.date = dt[i]
		}
	}
	as.POSIXct(all.extremes)
}
extreme = get.extreme.tides(new.first.set)

#abline(v=get.extreme.tides(new.first.set))

first.extreme = extreme[1]
dt2 = new.first.set$datetime
cycle.extremes = seq(first.extreme,dt2[length(dt2)],by=89400)
abline(v=cycle.extremes,lty="dashed")


exxxtreme = function() {
	extreme.lag = c(extreme, NA)
	extreme.early = c(extreme[1], extreme)
	extreme.early[1] = NA

	difference = extreme.lag - extreme.earl

	shapiro.test(as.numeric(difference))
	barplot(as.numeric(difference))
}



# zooreg(1:5,start=as.POSIXct("2014-01-01 01:00:00"))
# something to think about




# thoughts: 
#library("TTR")

#new.ts = SMA(tide.ts,n=700)
#plot.ts(new.ts)

#?stl
