# Plots specifically the map of NZ

library(maptools)
library(scales)
library(gpclib)
gpclibPermit()


# I did this manually - will change in 2015!
registers = c("WARD2014_N","UA2014_NAM","TASUB2014_","TA2014_NAM",
"REGC2014_N","MCON2014_N","CON2014_NA","CB2014_NAM","AU2014_NAM")
names(registers) = c("WARD2014_GV_Clipped.shp","UA2014_GV_Clipped.shp","TASUB2014_GV_Clipped.shp",
"TA2014_GV_Clipped.shp","REGC2014_GV_Clipped.shp","MCON2014_GV_Clipped.shp","CON2014_GV_Clipped.shp",
"CB2014_GV_Clipped.shp","AU2014_GV_Clipped.shp")

area.id = registers[shp.name]

# Paste together the GIS locations and the shape name
NZ.loc = paste(GIS.loc,shp.name,sep="/")
NZ.region = readShapeSpatial(NZ.loc)

# NZ.region@data to access meta data
# NZ.region[[area.id]] is same as $

# Order compact df to match the colours properly
compact.df = compact.df[order(factor(rownames(compact.df),levels = as.character(NZ.region[[area.id]]))),]

plot(NZ.region,col=compact.df$c1,main=finalTitle)

# Clearly need to sort compact.df by NZ.region... Use sort and a custom order
# http://stackoverflow.com/questions/17751886/sort-vector-of-integers-in-specific-custom-order


# Determine plot boundaries, in units of the data
xmin <- par("usr")[1]
xmax <- par("usr")[2]
ymin <- par("usr")[3]
ymax <- par("usr")[4]

xrange = range(xmin,xmax)
yrange = range(ymin,ymax)
xx = xmin + xrange/10
yy = ymax - yrange/10

legend(x = xx,y=yy,c("More Females","More Males","No Difference"),cex=0.8, 
        col=c("red","green","yellow"),pch=c(15))


read.shape.from.zip = function(area.zip,file.name) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(area.zip,exdir=temp.zip)
  shp = readShapePoly(paste(temp.zip,file.name,sep="/"))
  unlink(temp.zip)
  shp
}
