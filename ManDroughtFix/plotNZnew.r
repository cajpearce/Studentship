# Plots specifically the map of NZ

library(maptools)
library(scales)
library(gpclib)
gpclibPermit()

GIS.loc = "GISNZ2"
shp.name = "REGC2014_GV_Clipped"

# Plot NZ region map
NZ.loc = paste(GIS.loc,"/",shp.name,".shp",sep="")
NZ.region = readShapeSpatial(NZ.loc)

# NZ.region@data to access meta data
# TA2014_NAM territores
# REGC2014_N regional

NZ.region = NZ.region[NZ.region$REGC2014_N != "Area Outside Region",]
plot(NZ.region,	col=rgb(rnorm(15,0.5,0.1),rnorm(15,0.5,0.1),rnorm(15,0.5,0.1)),
	 	main="plot of NZ")

plot(new,col="green",add=TRUE)
