###Stats 380, Assignment 1, Chris Pearce (cpea714)

### Question 1 a)

next.term = function(x) {
	#the following is a failsafe for when x is a negative
	#if it starts at -12, it will add 1*2, therefore
	#next.term(-12) will return -10
	multiplier = 1
	if(x < 0) {multiplier = -1}
	x = abs(x)

	#converts the number to a string
	x.char = as.character(x)
	x.length = nchar(x.char)

	#creates a vector of the characters in the number
	x.vec = as.numeric(substring(x, 1:x.length, 1:x.length))
	
	#multiplies all the non-zero digits
	curr = 1
	for(i in 1:x.length) {
		if(x.vec[i] != 0) {
			curr = curr * x.vec[i]
		}
	}
	
	#special case of when x = 0, keeps x at 0 the whole way
	if(x == 0) {
		curr = 0
	}

	#applies the 'special case' and adds the product of the digits
	x + multiplier*curr
	
}

#test of next.term()
next.term(1032)

### Question 1 b)

dprodseq = function(x, nterm = 10) {
	#creates a vector of size (nterm), first value is the given value,
	#the following nterm-1 values are the successive next.term() values
	temp = x
	for (i in 1:(nterm-1)) {
		temp[i+1] = next.term(temp[i])
	}
	temp
}

#test of dprodseq()
dprodseq(10)
#dprodseq(10,20)


### Question 1 c)

dps20 = function(is.matrix=TRUE, n=20) {
	###written as a function, because I prefer the alignment of a matrix
	###when is.matrix = TRUE, printed as a matrix
	###when is.matrix = FALSE printed individual vectors in loop

	if(is.matrix) {
		top = matrix(dprodseq(1),nc=10)
		for(i in 2:n) {
			top = rbind(top, dprodseq(i))
		}
		print(top)
	} else {
		for(i in 1:n) {
			print(dprodseq(i))
		}
	}
}

#function call
dps20(TRUE)
#dps20(FALSE)


################################################
### Question 2

# Source: The Cambridge Factfinder, Cambridge University Press, 1993
# Language speakers in millions.

mother.tongue =
  c(1000, 350, 250, 200, 150, 150, 150, 135, 120,
    100, 70, 70, 65, 65, 60, 60, 55, 55, 50, 50)
names(mother.tongue) =
    c("Chinese", "English", "Spanish", "Hindi", "Arabic",
      "Bengali", "Russia", "Portuguese", "Japanese", "German",
      "French", "Panjabi", "Javanese", "Bihari", "Italian",
      "Korean", "Telugu", "Tamil", "Marathi", "Vietnamese")


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


#check the top of the function for a description of defaults values


###the function call to draw the example graph from handout
chris.plotter(mother.tongue,"Number of Speakers (Millions)")


###example of changing the default values (delete the hash tag, was annoying when running all)
#chris.plotter(mother.tongue, "THIS CAN BE CHANGED IN FUNCTION CALL",pch=1,ticks=10, labels=1:length(mother.tongue))
#chris.plotter(1000:980,"hello world",labels=1000:980,ticks=10,start.at.zero=FALSE)


