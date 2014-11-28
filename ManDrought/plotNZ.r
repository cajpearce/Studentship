# Plots specifically the map of NZ

library(maptools)
library(scales)
library(gpclib)
gpclibPermit()

read.shape.from.zip = function(area.zip,file.name) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(area.zip,exdir=temp.zip)
  shp = readShapePoly(paste(temp.zip,file.name,sep="/"))
  unlink(temp.zip)
  shp
}

# need shapeList and colours
# this should be standalone in plotRegions.r
plot.regions = function(shape.l, colours) {
  for (i in 1:length(shape.l)) {
    inner.shapes = shape.l[[i]]
    for(j in 1:length(inner.shapes)) {
      plot(inner.shapes[[j]],add=TRUE,col=colours[i],border=FALSE)
    }
  }
}


# Plot NZ region map
NZ.loc = paste(GIS.loc,"NZ/NZ_L2_2006_NZMG_ArcShp.zip",sep="/")
NZ.region = read.shape.from.zip(NZ.loc,"TA06_LV2_V2.shp")
plot(NZ.region,xlim=c(2059004,3003022),
          ylim=c(5301970,6766245))


#this should be standalone in plotRegions.r
plot.regions(shapeList,compact.df$c1)
legend(x=2100000,y=6666245,c("More Females","More Males","No Difference"),cex=.8, 
        col=c("red","green","yellow"),pch=c(15))
