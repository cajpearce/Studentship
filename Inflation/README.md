The precursor to Pyflation but written in the R programming language.
<b>Preface:</b>

<b>Module 1 - inflation.r:</b>

Download spreadsheet from the reserve bank, take the right worksheet, grab the
USD information. Difference between this and Pyflation is that I keep all the
information in the R version, because it's so simple to.

Uses gdata's read.xls function to read an excel file, uses zoo to create the
date column. Useful later when creating a lowess curve.

<b>Module 2 - prettyDF.r:</b>

A really simple module that's fairly generic, removes columns with 1 dimensional
data. May be destructive but normally 1 dimensional columns are uninformative
when taken from the internet due to the way html structures data.

<b>Module 3 - htmlscraper.r:</b>
	
Read a wikipedia page (original html version) and takes the biggest wikipedia 
table on that page. Cleans it up a bit then assigns colours to the parties.

Not very generic but could probably split up the wikipedia processing.

Uses XML to read the webpage, scales to create the colours with alpha values.

Definitely easier than python.

<b>Module 4 - plotter.r:</b>

Plots the graph, creates the colour terms by year (not term) then plots a lowess
curve.


<b><u>Code follow-through:</u></b>

<b>Module 1 - inflation.r:</b>
```
library(gdata)
library(zoo)

df = read.xls("http://www.rbnz.govt.nz/statistics/key_graphs/graphdata.xls",
		sheet = 8, header = TRUE,skip=2,row.names=2)
```
Reads the excel spreadsheet from reserve bank into a dataframe.

```
yearly = gsub("M.*$","",rownames(df))
monthly = gsub("^.*M","",rownames(df))
monthly = sprintf("%02s", monthly)

new.dates = as.yearmon(paste(yearly,monthly,sep="-"))
rownames(df) = new.dates

df$Year = format(new.dates, "%Y")
df$Date = new.dates

df$USD = zoo(df$R.USD,df$Date)
```
Finds the years and the months, pads the months with zeroes to length 2, then
turns it into a yearmon format as found in the zoo library. Sets these as the
rownames, but also creates a column for it and also assigns the years.

In retrospect this was probably an unnecessary amount of duplication but it's so
easy to manipulate data in R that frankly I don't care.

Note that I probably should've used strsplit instead of gsub but after using
sapply(strsplit(...),'[[',1) then same with 2, it would have been just as many
lines and less readable.

In the end it turns USD into a zoo function so that it can be lowessed later.


<b>Module 2 - prettyDF.r:</b>
```
# Cleans up a dataframe by removing unnecessary columns with useless input
########## Module

remove.1D.cols = function(data) {
	factored.data = lapply(data, factor)
	nleveler = Vectorize(nlevels)
	data[!(nleveler(factored.data) <= 1)]
}

# Get rid of the unnecessary columns (1 dimensional/no information)
compact.df = remove.1D.cols(df)
```

Checks for 1 dimensional columns by turning each column into a factor then
removing them if the levels is less than or equal to 1.

<b>Module 3 - htmlscraper.r:</b>
```
library(XML)
library(scales)
theurl <- "http://en.wikipedia.org/wiki/New_Zealand_Parliament"
tables <- readHTMLTable(theurl)
n.rows <- unlist(lapply(tables, function(t) dim(t)[1]))

nzp = data.frame(tables[[which.max(n.rows)]])
```
Pretty simple stuff really. reads all the tables from a wikipedia page using the
XML library. the n.rows... part just using the dim function to find the largest
table by how much it contains, then assigns it to nzp.

```
names(nzp) = c("Term","Year","Government")
nzp$Term = as.character(nzp$Term)

#Get rid of years that don't exist
nzp = nzp[!is.na(nzp$Year),]

# Turn year it into a number
nzp$Year = as.numeric(gsub("[ a-zA-Z]*$","",nzp$Year))
```
Pretty self-explanatory with the comments. the gsub works because it removes all
letters and spaces then converts it to a number.

```
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
```
Exact same functionality as in PyFlation. Reading the table from the wiki
has NAs on subsequent terms, so need to pad out the NAs with the current govt.

I.e. it only lists the government when they first come into power, we want
WHENEVER they're in power.

```
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
```

Pretty obvious; adds a colour vector based on the party in power. Can be
manipulated easily to give unique colours to all parties, past and present.

```
fin = length(nzp$Year)
add.term = nzp[fin,]
nzp[fin + 1,] = add.term
nzp[fin + 1,"Year"] = 2017
```
Duplicates the final row and adds it with the year 2017... Pretty hacky 
manoeuvre but i mean, the national government is prooooobably going to be around
till 2017 and this is just a hack way of making sure the entire plot is coloured


<b>Module 4 - plotter.r:</b>


:)
