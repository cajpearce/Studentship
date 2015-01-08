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

download.locations = paste(root.link,identifiers,"/",year,"/",identifiers,sep="")



top = "http://apps.linz.govt.nz/ftp/sea_level_data/AUCT/2014"

day.numbers = str_pad(1:365, 3, pad = "0")
dates = paste(year,day.numbers,sep="")

all.downloads = lapply(download.locations, paste, "_",dates,".zip",sep="")
all.csvs = lapply(identifiers,paste,"_",dates,".csv",sep="")

################################################################################
# 	CAN SPLIT HERE
################################################################################
#	but won't :)
################################################################################

# Using code from ManDrought

read.csv.from.zip = function(file.zip,csv.name) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(file.zip,exdir=temp.zip)
  measurements = read.csv(csv.name)
  unlink(temp.zip)
  measurements
}

