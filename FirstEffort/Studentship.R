library(maptools)
library(scales)


# Read the CSV into R
########## Module
age.sex.df = read.csv("sexagedata.csv",header=T)

remove.1D.rows = function(data) {
	factored.data = lapply(data, factor)
	nleveler = Vectorize(nlevels)
	data[!(nleveler(factored.data) <= 1)]
}

xtabs
# Get rid of the unnecessary columns (1 dimensional/no information)
#compact.df = age.sex.df[-c(2,3,6)]
compact.df = remove.1D.rows(age.sex.df)
############


# Create a contingency table of Value by area and sex
# could!!! could create a factor of each. find most variable data (numerical?)
compact.tab = xtabs(Value~Area+Sex,data=compact.df)
compact.df = as.data.frame(unclass(compact.tab))

# Rename to make it prettier
names(compact.df) = c("Female","Male","Total")


# Add a column for the percentage of females by total
compact.df$percentage = compact.df$Female/compact.df$Total

# Perform a Proportion test on all the 
# doing prop.test on a vector just returns proportions; need to do it individually to get p-values
pt.pvalues = function(v1, v2) {
  count = numeric(0)
  for (i in 1:length(v1)) {
    p.val = prop.test(v1[i],v2[i])$p.value
    count = c(count, p.val)
  }
  count
}

compact.df = cbind(compact.df,p.values = pt.pvalues(compact.df$Female,compact.df$Total))



# Creates a colour for P-values - should defo be customised
########### MODULE
num.bind = function(v1, low=0, high=1) {
	v1[v1 < 0] = 0
	v1[v1 > 1] = 1
	v1
}

cor(compact.df)

colour.function = function(p.values, v1, midpoint=0.5) {
	indices = log10(1.05 - p.values)/log10(1.05)	
	indices = num.bind(indices) * 0.9
	logical.lower = v1 < midpoint
	cols = ifelse(v1 < midpoint, rgb(0,1,0,alpha=indices),rgb(1,0,0,alpha=indices))
	cols[indices == 0] = rgb(1,1,0,alpha = 0.2)
	cols
}

compact.df$c1 = colour.function(compact.df$p.values,compact.df$percentage)
###########



# Map time!

# creates a list of all shape files from the zips provided to the below function


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
    shp = readShapePoly(f)
    shp.list = c(shp.list,shp)
  }
  unlink(temp.zip)
  list(shp.list)
}



plot.regions = function(shape.l,colours) {
  for (i in 1:length(shape.l)) {
    inner.shapes = shape.l[[i]]
    for(j in 1:length(inner.shapes)) {
      plot(inner.shapes[[j]],add=TRUE,col=colours[i],border=FALSE)
    }
  }
}

#map('nzHires')#,xlim=c(166,179),ylim=c(-48,-34))

read.shape.from.zip = function(area.zip,file.name) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(area.zip,exdir=temp.zip)
  shp = readShapePoly(paste(temp.zip,file.name,sep="/"))
  unlink(temp.zip)
  shp
}


# Plot NZ region map
NZ.region = read.shape.from.zip("GIS/NZ/NZ_L2_2006_NZMG_ArcShp.zip","TA06_LV2_V2.shp")
plot(NZ.region,xlim=c(2059004,3003022),
          ylim=c(5301970,6766245))

shapeList = read.shapes("GIS/Regions")

#pdf("colour.pdf")

plot.regions(shapeList,compact.df$c1)
legend(x=2100000,y=6666245,c("More Females","More Males","No Difference"),cex=.8, 
        col=c("red","green","yellow"),pch=c(15))
#dev.off()

