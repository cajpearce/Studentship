library(XML)
library(scales)
theurl <- "http://en.wikipedia.org/wiki/New_Zealand_Parliament"
tables <- readHTMLTable(theurl)
n.rows <- unlist(lapply(tables, function(t) dim(t)[1]))

nzp = data.frame(tables[[which.max(n.rows)]])

names(nzp) = c("Term","Year","Government")
nzp$Term = as.character(nzp$Term)

#Get rid of years that don't exist
nzp = nzp[!is.na(nzp$Year),]

# Turn year it into a number
nzp$Year = as.numeric(gsub("[ a-zA-Z]*$","",nzp$Year))

padNames = function(str) {
	str = as.character(str)

	current = ""
	for (i in 1:length(str)) {
		if (is.na(str[i])) {
			str[i] = current
		} else if (current != str[i]) {
			current = str[i]
		}
	}
	str
}

nzp$Government = padNames(nzp$Government)


blue = rgb(0.25,0.25,1,alpha=0.2)
red = rgb(1,0.25,0.25,alpha=0.2)
green = rgb(0.25,1,0.25,alpha=0.2)

colourFunction = function(partyStr) {
	lab.id = grep("Labour",partyStr)
	nat.id = grep("National",partyStr)

	col = rep(green,length(partyStr))
	col[lab.id] = red
	col[nat.id] = blue
	col
}

nzp$Col = colourFunction(nzp$Government)
