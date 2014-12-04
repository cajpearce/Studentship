png("inflation.png",width=640)
plot(compact.df$Date, compact.df$R.USD,
	xlab="Date",ylab="NZD to USD conversion rate",main="NZD value over time")
my.seq = seq(1,length(compact.df[,1]),by=12*5)

#abline(v=compact.df$Date[my.seq],lty="dashed")
abline(h=1)
for(i2 in 2:length(nzp$Col)) {
	i = i2 - 1
	xl = nzp$Year[i]
	xr = nzp$Year[i2]
	y1 = -1
	y2 = 10

	rect(xl,y1,xr,y2,col=nzp$Col[i],border=nzp$Col,lwd=0)

	if(nzp$Col[i2] != nzp$Col[i]) {
		abline(v=nzp$Year[i2],lty="dashed",lwd=2)
	}
}

rect(2014,-1,2017,10,col=blue,border=blue,lwd=0)

dev.off()
