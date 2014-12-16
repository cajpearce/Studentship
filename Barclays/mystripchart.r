mystripchart = function(dataframe,...) {
	plot.new()
	plot.
}

chris.plotter = function(data, xlabel="x", pch=16, ticks=5, labels=names(data),start.at.zero=TRUE) {
	
	####################
	#PLEASE NOTE
	#
	#if negatives numbers are in your dataset,
	#the graph will start from the lowest value and there will be a tick
	#to show what the lowest value is
	#
	#otherwise, if all positive, the graph automatically starts at 0
	#unless start.at.zero is set to FALSE
	#in which case it follows the same standard as for negative numbers
	####################
	
	#brief description of args:
		# data to be plotted
		# xlabel sets the x axes annotation, default is "x"
		# pch changes the plotting symbol (default is a solid circle)
		# ticks is the number of ticks on the x axes, default is 5
		# labels is the labels on the y axis, default is names of the vector provided in default
		# starts.at.zero: if TRUE, forces the plot to x axis to start at 0 if all positive data, if FALSE starts at the lowest value of data



	### get rid of the margins
	opar = par(mfrow = c(1, 1), mar = rep(0, 4), cex = 1)


	### set out the layout of the plot
	layout(matrix(c(0, 0, 0, 0,
			    0, 0, 3, 0,
			    0, 2, 1, 0,
			    0, 0, 4, 0,
			    0, 0, 0, 0),
			    nc=4, byrow=TRUE),
		widths= c(lcm(1), lcm(3), 1, lcm(1)),
		heights=c(lcm(1), lcm(2), 1, lcm(2), lcm(2)))
	

	### set the magnification
	par(cex=1)

	
	###sets up data for the limits of the plot
	xlim = range(data)
	y = 1:length(data)
	ylim = range(y)
	

	### plot.xlim calculated because we will be using xaxs="i" - see later
	plot.xlim = c(0,xlim[2])
	
	if(xlim[1] < 0 || !start.at.zero) {
		plot.xlim[1] = xlim[1]
	}
	
	plot.diff = plot.xlim[2] - plot.xlim[1]
	plot.xlim[2] = xlim[2] + plot.diff*0.025


	### Create the plot window
	### uses xaxs="i" so the function works with small data values too (around 0)
	plot.new()
	plot.window(xlim=plot.xlim, ylim=rev(ylim), xaxs="i")


	### Sets up the outline of the plot, with axes
	### axes set up so they work with negative numbers
	sep = plot.diff/ticks
	include.zero = sep
	if(xlim[1] < 0 || !start.at.zero) {
		include.zero = 0
	}
	axis(1, c(seq(plot.xlim[1]+include.zero, plot.xlim[2], by=sep)))
	axis(3, c(seq(plot.xlim[1]+include.zero, plot.xlim[2], by=sep)))
	box()

	#draws the lines to the dots, then draws the actual dots
	segments(plot.xlim[1], y, data, y,
			lty = "dotted", lwd = par("lwd"))
	points(data, y, pch=pch)


	### sets up the plot for the labels to the left
	plot.new()
	plot.window(xlim=c(0,1), ylim =rev(ylim),
		xaxs="i")

	## draws the labels
	text(1, y, labels=labels,pos=2)


	### next two plots just draw the axes labels (top and bottom x-axis)
	plot.new()
	plot.window(xlim=c(0,1),ylim=c(0,1))
	text(0.5,0.9,labels=xlabel)

	plot.new()
	plot.window(xlim=c(0,1),ylim=c(0,1))
	text(0.5,0.1,labels=xlabel)


	### resets graphics
	par(opar)
}
