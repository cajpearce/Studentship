#png("inflation.png",width=640)
library(zoo)

mycols = c("red","orange","yellow","darkgreen","blue","purple","black")

ymin = min(df[,-1])
ymax = max(df[,-1])

plot(df$Year, df[,2], xlab="Year",
	col=mycols[1],ylim=c(ymin,ymax))


for(i2 in 2:length(nzp$Col)) {
	i = i2 - 1
	xl = nzp$Year[i]
	xr = nzp$Year[i2]
	y1 = par("usr")[3]
	y2 = par("usr")[4]

	rect(xl,y1,xr,y2,col=nzp$Col[i],border=nzp$Col[i],lwd=0)

	if(nzp$Col[i2] != nzp$Col[i]) {
		abline(v=nzp$Year[i2],lty="dashed",lwd=2,col='black')
	}
}

#dev.off()
points(df$Year, df[,3],col=mycols[2])
points(df$Year, df[,4],col=mycols[3])


for (i in 1:length(mycols)) {
	y.lo <- loess(df[,i + 1] ~ df$Year, span=0.2)
	lo = predict(y.lo,df$Year)
	points(df$Year, df[,i + 1],col=mycols[i])
	lines(df$Year,lo,col=mycols[i],lwd=2)
}
