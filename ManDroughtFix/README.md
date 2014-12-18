Make sure to change dat.r
  -	CSV.loc and GIS.loc need to be absolute paths
  -	Don't change anything else

Make sure to download the GIS data from...
  -	http://www3.stats.govt.nz/digitalboundaries/annual/ESRI_Shapefile_Digital_Boundaries_2014_Generalised_Clipped.zip
  -	Save it as GISNZ in the directory (or save it anywhere and point GIS.loc
	to the directory)


Plotting the ManDrought using GIS data from stats.govt.nz and information from
the 2013 census.

<b>Preface:</b>

<b>Module 0 - dat.r</b>

Barely a module, defines some configuration for the rest of the application.
Due to limitations currently in OpenAPI, for programs using additional files
you must define path files manually as you pass it between computers. dat.r just
defines some file configuration and passes it to the modules where it is needed.

<b>Module 1 - prettyCSV.r:</b>

Opens up the data, applies my (reused) fairly generic function remove 1D cols
which I've turned into its own module in later pipeline examples (Inflation).
Because of the way data is structured on NZ.stat i've written a quick piece of
code that turns it into a more useable format.

<b>Module 2 - createPercentagePValues.r:</b>

Performs a proportion test on the data and saves it in the dataset so it can be
used when generating the colours for the map of New Zealand.

<b>Module 3 - colourCreator.r:</b>

Generates the colours to be used by the map based on the P-values. This module 
is hybrid generic and would only require a little bit of modification to use it
elsewhere.

<b>Module 4 - plotNZnew.r:</b>

Actually plots the information over the map of new zealand. The map data can be
downloaded from http://www3.stats.govt.nz/digitalboundaries/annual/ESRI_Shapefile_Digital_Boundaries_2014_Generalised_Clipped.zip


<b><u>Code follow-through:</u></b>

<b>Module 0 - dat.r</b>

```
CSV.loc ="~/Studentship/ManDroughtFix/agesexdata.csv"
GIS.loc ="~/Studentship/ManDroughtFix/GISNZ"
shp.name="TA2014_GV_Clipped.shp"
title	="Age"
```

Defines some configuration for the rest of the pipeline. CSV.loc is the absolute
path file to the CSV file (can use different age groups if downloaded from
NZ.stat. GIS information downloaded from http://www3.stats.govt.nz/digitalboundaries/annual/ESRI_Shapefile_Digital_Boundaries_2014_Generalised_Clipped.zip and unzipped.

<b>Module 1 - prettyCSV.r:</b>

```
age.sex.df = read.csv(CSV.loc,header=T)

remove.1D.cols = function(data) {
	factored.data = lapply(data, factor)
	nleveler = Vectorize(nlevels)
	data[!(nleveler(factored.data) <= 1)]
}

# Get rid of the unnecessary columns (1 dimensional/no information)
compact.df = remove.1D.cols(age.sex.df)
```

Reads the data in from the CSV file then removes columns with no useful info.
This can happen where you're downloading information from the internet due to
data being generic so there can be NA columns which are used in other datasets.

```
compact.tab = xtabs(Value~Area+Sex,data=compact.df)
compact.df = as.data.frame(unclass(compact.tab))
```

Uses cross tabs to make the information pretty, as it is stored as a contingency
table on NZ.stat but doesn't save well as a CSV.

```
# Rename to make it prettier
names(compact.df) = c("Female","Male","Total")

getTitle = function(title, data) {
	factored.column = factor(data[,title])
	paste(title,levels(factored.column),sep=": ",collapse=" ")
}

finalTitle = getTitle(title,age.sex.df)
```
As it says, makes it pretty. Also uses the original (non cleaned) data to get
the title. Fairly generic function, just takes a column name and takes the 1 dim
information from it and passes it on.

<b>Module 2 - createPercentagePValues.r:</b>
```
pt.pvalues = function(v1, v2) {
  count = numeric(0)
  for (i in 1:length(v1)) {
    p.val = prop.test(v1[i],v2[i])$p.value
    count = c(count, p.val)
  }
  count
}

compact.df$percentage = compact.df$Female/compact.df$Total
compact.df = cbind(compact.df,p.values = pt.pvalues(compact.df$Female,compact.df$Total))
```
Vectorised function performing a prop test on all the territories (or whatever
area unit you've picked). Normally would use 'apply' or some other vectorised
form but the p.values are stored secondary to the expected proportion so found
this easier. then assigns a percentage and the p values to compact.df. 
Es simplemente!

<b>Module 3 - colourCreator.r:</b>
```
num.bind = function(v1, low=0, high=1) {
	v1[v1 < 0] = 0
	v1[v1 > 1] = 1
	v1
}
```

small function to bind a number between two other numbers - ie if below low (0)
it sets it to 0, if above high (1) it sets it to 1. Keeps it between 1 and 0 for
the colour since the RGB values run between 0 and 1.

```
colour.function = function(p.values, v1, midpoint=0.5, cutoff=0.05, offset = 0.01) {
	indices = log10(1 + cutoff + offset - p.values)/log10(1 + cutoff + offset)	
	indices = num.bind(indices)
	cols = ifelse(v1 < midpoint, rgb(0,1,0,alpha=indices), rgb(1,0,0,alpha=indices))
	cols[p.values > cutoff] = rgb(1,1,0,alpha = 0.2)
	cols
}
```
Uses logs to create a nice colour gradient since P-value interpretation
generally follows a pretty non-linear distribution. The p.values are provided,
V1 and midpoint are to determine whether the colour is red or green (so gives
different colours depending if there is a man drought or woman drought), the
cutoff determines the different levels of interpretation based on p.values.
0.95 is 95% confidence, 0.99 would be 99% confidence. Offset is just to make 
sure that the colours aren't completely empty when close to the cutoff. Without
the offset, if your p-value was 0.499 the colour would be almost white. The
offset makes sure it's still slightly green (or red).

<b>Module 4 - plotNZnew.r:</b>
```
library(maptools)
library(scales)
library(gpclib)
gpclibPermit()
```
Brings all the libraries in, gpclibPermit() just allows you to plot as there is
apparently some restriction on GIS data.

```
# I did this manually - will change in 2015!
registers = c("WARD2014_N","UA2014_NAM","TASUB2014_","TA2014_NAM",
"REGC2014_N","MCON2014_N","CON2014_NA","CB2014_NAM","AU2014_NAM")
names(registers) = c("WARD2014_GV_Clipped.shp","UA2014_GV_Clipped.shp","TASUB2014_GV_Clipped.shp",
"TA2014_GV_Clipped.shp","REGC2014_GV_Clipped.shp","MCON2014_GV_Clipped.shp","CON2014_GV_Clipped.shp",
"CB2014_GV_Clipped.shp","AU2014_GV_Clipped.shp")

area.id = registers[shp.name]
```

A 'dictionary' in a way linking the name of the file used with the column ID
for the locations. Used to compare the locations in the GIS data with the
locations in the CSV file you've provided so you can merge on this and draw
accurate colours for accurate areas.

```
# Paste together the GIS locations and the shape name
NZ.loc = paste(GIS.loc,shp.name,sep="/")
NZ.region = readShapeSpatial(NZ.loc)

# NZ.region@data to access meta data
# NZ.region[[area.id]] is same as $

# Order compact df to match the colours properly
compact.df = compact.df[order(factor(rownames(compact.df),levels = as.character(NZ.region[[area.id]]))),]

plot(NZ.region,col=compact.df$c1,main=finalTitle)
```
Comments explain it pretty well. the latter just merges upon area name from the
above code segment, then plots it. A lot of this stuff is passed from dat.r.

```
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
```
Plots a legend using plot dimensions. Doesn't do it very well though.

```
read.shape.from.zip = function(area.zip,file.name) {
  temp.zip = tempfile()
  dir.create(temp.zip)
  unzip(area.zip,exdir=temp.zip)
  shp = readShapePoly(paste(temp.zip,file.name,sep="/"))
  unlink(temp.zip)
  shp
}
```
Final piece of code is unused at the moment, but could be implemented either in
its own module or otherwise. Reads a shape from a ZIP file into a temporary 
directory then reads the shape from there. Would mean the end user would not
need to extract the data themselves. Could even be used to download the data
automatically.

:)
