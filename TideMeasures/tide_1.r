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
