# Cleans up a dataframe by removing unnecessary columns with useless input
########## Module

remove.1D.cols = function(data) {
	factored.data = lapply(data, factor)
	nleveler = Vectorize(nlevels)
	data[!(nleveler(factored.data) <= 1)]
}

# Get rid of the unnecessary columns (1 dimensional/no information)
compact.df = remove.1D.cols(df)

