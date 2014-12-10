### Plots of the teams in Premier League over past decade

link = "http://www.football-data.co.uk"

### read in the webpage
webpage = readLines(paste(link,"englandm.php",sep="/"))
print(paste("Downloaded main HTML page from:",link))
### get the index of the titles
season.index = grep("Season", webpage)
premier.index = season.index + 1

html.shortlist = webpage[premier.index]

### process them down to readable URLs
csv.links = gsub("^.*<A HREF=\\\"","",html.shortlist)
csv.links = gsub("\".*$","",csv.links)
csv.links = paste(link,csv.links,sep="/")

### Global
csv.data = sapply(csv.links,read.csv,header=T)
print(paste("Downloaded",length(csv.links),"CSV files."))

teams = lapply(csv.data, '[[', "HomeTeam")
unique.teams = sapply(teams,levels)
years = 2015 - 1:22
names(unique.teams) = years

### Data cleaning = getting rid of empty strings
for(i in 1:22) {
  un = unique.teams[[i]]
  un = un[!(un %in% "")]
  unique.teams[[i]] = un
}


### getting all unique team names
all.teams = levels(factor(unlist(unique.teams)))
unique.df = data.frame(row.names=all.teams)

### creating data
for(i in unique.teams) {
  unique.df = cbind(unique.df, as.numeric(table(c(all.teams,i))) - 1)
}

### creating dataframe
names(unique.df) = years
unique.df = data.frame(t(unique.df))
row.names(unique.df) = years

#plot(unique.df$Aston.Villa,type="o")
#write.csv(unique.teams, "C:/Users/Christopher/Documents/Programming")


### making the 1s useful: creating a unique ID for each team
for(i in 1:length(unique.df[1,])) {
  temp = unique.df[,i]
  temp[temp==1] = years[temp==1] #change me to i
  unique.df[,i] = temp
}

### changing all zeroes to NA to signify they're not there
unique.df[unique.df == 0] = NA


stripchart(unique.df,vertical=TRUE,pch=16,type="l")

