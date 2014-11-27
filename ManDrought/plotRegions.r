# Specifically plot regions from shapeList passed in from zipShapeReader.r
# Should always run plotNZ.r first if borders are desired

library(maptools)
library(scales)

plot.regions = function(shape.l,colours) {
  for (i in 1:length(shape.l)) {
    inner.shapes = shape.l[[i]]
    for(j in 1:length(inner.shapes)) {
      plot(inner.shapes[[j]],add=TRUE,col=colours[i],border=FALSE)
    }
  }
}

plot.regions(shapeList,compact.df$c1)
legend(x=2100000,y=6666245,c("More Females","More Males","No Difference"),cex=.8, 
        col=c("red","green","yellow"),pch=c(15))
