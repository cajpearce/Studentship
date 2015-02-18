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

all.tides = check.cache("~/Studentship/TideMeasures/alltides.rds")
