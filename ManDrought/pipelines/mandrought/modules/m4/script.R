setwd("/home/cpea714/Studentship/ManDrought/pipelines/mandrought/modules/m4")
loc <- ""
# creates a list of all shape files from the zips provided to the below function
library(maptools)
library(gpclib)
gpclibPermit()

read.shapes = function(loc) {
  shape.l = list()
 
  area.files = create.zip.list(loc)

  for (af in area.files) {
    print(af)
    shps = read.shapes.from.zip(af)
    shape.l = c(shape.l,shps)
  }
  shape.l
}

# Goes to the location and creates a directory listing of all zip files
create.zip.list = function(loc) {
	f.list = list.files(loc)
	paste(loc,f.list[grep("zip$",f.list)],sep="/")
}

read.shapes.from.zip = function(area.zip) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(area.zip,exdir=temp.zip)
  
  orig.files = list.files(temp.zip)
  
  s.files = orig.files[grep("^AU_TA.+shp$",orig.files)]
  s.files = paste(temp.zip,s.files,sep="/")
  
  shp.list = list()
  for (f in s.files) {
    #print(paste("+ ",f))
    shp = readShapePoly(f)
    shp.list = c(shp.list,shp)
  }
  unlink(temp.zip)
  list(shp.list)
}

shapeList = read.shapes("~/Studentship/ManDrought/GIS/Regions")
saveRDS(shapeList, file="shapeList.rds")
