# at the mo 
first.set = all.tides[[which(identifiers == "AUCT")]]
second.set = all.tides[[which(identifiers == "TAUT")]]


# the following snippit just gets the first 7 days of tides from first & second
days = 7
# assigns first day
new.first.set = first.set[[1]]
new.second.set = second.set[[1]]
# then iterates through the next 6 days
for(i in 2:days) {
	new.first.set = rbind(new.first.set,first.set[[i]])
	new.second.set = rbind(new.second.set,second.set[[i]])
}


# making sure both datasets fit into the same plot
ymin = min(new.first.set$height,new.second.set$height)
ymax = max(new.first.set$height,new.second.set$height)

# plot both!
#plot(new.first.set$datetime,new.first.set$height,ylim = c(ymin,ymax),type="l")
#lines(new.second.set$datetime,new.second.set$height,col="red")


tide.ts = ts(new.first.set$height)
acf(tide.ts,lag.max=length(tide.ts)/7)
spectrum(tide.ts,spans=c(3,5))
