# Read the CSV into R
########## Module

age.sex.df = read.csv(CSV.loc,header=T)

remove.1D.rows = function(data) {
	factored.data = lapply(data, factor)
	nleveler = Vectorize(nlevels)
	data[!(nleveler(factored.data) <= 1)]
}

# Get rid of the unnecessary columns (1 dimensional/no information)
compact.df = remove.1D.rows(age.sex.df)
############


############ This is more specific so could go elsewhere

# Create a contingency table of Value by area and sex
# could!!! could create a factor of each. find most variable data (numerical?)
compact.tab = xtabs(Value~Area+Sex,data=compact.df)
compact.df = as.data.frame(unclass(compact.tab))

# Rename to make it prettier
names(compact.df) = c("Female","Male","Total")

getTitle = function(title, data) {
	factored.column = factor(data[,title])
	paste(title,levels(factored.column),sep=": ",collapse=" ")
}

finalTitle = getTitle(title,age.sex.df)
