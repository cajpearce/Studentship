# read in the top page that contains references to all possible measurements
original.link = "http://www.linz.govt.nz/sea/tides/sea-level-data/sea-level-data-downloads"
root.link = "http://apps.linz.govt.nz/ftp/sea_level_data/"

year = 2014

# reads in the original page
original.page = readLines(original.link)

# finds all hyperlinks starting with http://apps.linz.govt.nz/ftp/sea_level_data/
line.with.links = grep(root.link, original.page,value=TRUE)

# it's only 1 line long... who wrote this webpage?!

# Split it where the link starts, so I can use GSUB
link.splits = strsplit(line.with.links, root.link)
link.splits = unlist(link.splits)

# uses GSUB to remove everything after the potential identifiers
identifiers = gsub("/.*$","",link.splits)

# Get rid of the annoying first link. A little over the top, but more generic
identifiers = identifiers[grepl("^[A-Z]+$",identifiers)]


# Collapse them down to unique identifiers
identifiers = levels(factor(identifiers))




################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################

library(stringr)

# Creates a list of the webpages where downloads are found (each IDENTIFIER has
# its own webpage which contains the measurements
download.locations = paste(root.link,identifiers,"/",year,"/",identifiers,sep="")

# need to pad zeroes onto 1-99 using library(stringr)
day.numbers = str_pad(1:365, 3, pad = "0")

# need to paste the year onto each day (001-365)
dates = paste(year,day.numbers,sep="")

# paste together the top page of each individual identifier with the zip file
all.downloads = lapply(download.locations, paste, "_",dates,".zip",sep="")

#similar but just adds .csv (since this is what's inside each zip file
all.csvs = lapply(identifiers,paste,"_",dates,".csv",sep="")

################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################

# Using code from ManDrought
# tryCatch has been customised, otherwise it's pretty universal
read.csv.from.zip = function(file.zip,csv.name,return.as.list=TRUE) {
	temp = tempfile()
	measurements = data.frame(id=numeric(0),datetime=numeric(0),height=numeric(0))

	download.file(file.zip,temp,quiet=TRUE)
	
	tryCatch({	# This is customised!!! Won't work for individual CSVs
			measurements = read.csv(unz(temp,csv.name),
					col.names=c("id","datetime","height"))
			measurements$datetime = as.POSIXct(measurements$datetime)
			},
			error=function(e) {print(paste("ERROR:",file.zip))},
			warning=function(w) {print(paste("WARNING:",file.zip))})

	unlink(temp)

	if(return.as.list) {
		measurements = list(measurements)
	}
	measurements
}

# vectorises it so can be used in mapply in check.cache()
vec.read = Vectorize(read.csv.from.zip)


# because this program reads in 365 * 18 zip files, I'd prefer it be saved
# checks to see if it can load it from an RDS file first
check.cache = function(name="alltides.rds",save=name) {
	temp = ""
	if (file.exists(name)) {
		temp = readRDS(name)
	} else {
		temp = mapply(vec.read, all.downloads,all.csvs,SIMPLIFY=FALSE)
		saveRDS(temp,save)
	}
	temp
}

all.tides = check.cache()


################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################

# at the mo 
first.set = all.tides[[which(identifiers == "AUCT")]]
second.set = all.tides[[which(identifiers == "TAUT")]]


# the following snippit just gets the first 7 days of tides from first & second

# assigns first day
new.first.set = first.set[[1]]
new.second.set = second.set[[1]]
# then iterates through the next 6 days
for(i in 2:7) {
	new.first.set = rbind(new.first.set,first.set[[i]])
	new.second.set = rbind(new.second.set,second.set[[i]])
}


# making sure both datasets fit into the same plot
ymin = min(new.first.set$height,new.second.set$height)
ymax = max(new.first.set$height,new.second.set$height)

# plot both!
plot(new.first.set$datetime,new.first.set$height,ylim = c(ymin,ymax),type="l")
lines(new.second.set$datetime,new.second.set$height,col="red")


################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################
library(zoo)
z1 = zoo (new.first.set$height, new.first.set$datetime)
z2 = zoo (new.second.set$height, new.second.set$datetime)
m = merge(z1, z2)


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
abline(v=get.extreme.tides(new.first.set))

extreme.lag = c(extreme, NA)
extreme.early = c(extreme[1], extreme)
extreme.early[1] = NA

print(extreme.lag - extreme.early)

# zooreg(1:5,start=as.POSIXct("2014-01-01 01:00:00"))
# something to think about




# thoughts: 
#library("TTR")

#new.ts = SMA(tide.ts,n=700)
#plot.ts(new.ts)

#?stl
