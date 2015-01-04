#png("inflation.png",width=640)
plot(df$Year, df$SocialAndWelfare, xlab="Year",ylab="Social and Welfare as % of GDP")


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

#rect(2014,-1,2017,10,col=blue,border=blue,lwd=0)

years = 12

lo = lowess(compact.df$USD, f = (12*years)/length(compact.df$Date))
lines(index(compact.df$USD),lo$y,lwd=4,col="green")
#dev.off()
