### Morbid, but relatively interesting
### Sourced from http://www.health.govt.nz/publication/mortality-historical-summary-1948-2010
### And from http://www.stats.govt.nz/

suicide.df = read.csv("suicide.csv")
population.df = read.csv("population.csv")
unemployment.df = read.csv("unemployment.csv")
GDP.df = read.csv("GDP.csv")
birthrates.df = read.csv("birthrates.csv")
crime.df = read.csv("crime.csv")
marriage.df = read.csv("marriage.csv")

suicide.df = suicide.df[c("Year","Suicide.Total")]
population.df = population.df[c("Year","Pop.Total")]
#unemployment.df = unemployment.df[c("Year","Unemployment.Male","Unemployment.Female","Unemployment.Total")]
year.min = 1986
year.max = 2010

pop.min = which(population.df$Year == year.min)
pop.max = which(population.df$Year == year.max)
sui.min = which(suicide.df$Year == year.min)
sui.max = which(suicide.df$Year == year.max)
sui.df = suicide.df[sui.min:sui.max,]
clean.df = population.df[pop.min:pop.max,]

clean.df[-1] = sui.df[-1]/clean.df[-1]
clean.df = cbind(clean.df,unemployment.df[-1])
clean.df = cbind(clean.df,GDP.df[-1])
clean.df = cbind(clean.df,birthrates.df[-1])
clean.df = cbind(clean.df,crime.df[-1])
clean.df = cbind(clean.df,marriage.df[-1])

clean.df = clean.df[-1]
clean.lm = lm(Pop.Total~.,data=clean.df)

clean.lm=lm(Pop.Total~Unemployment.Male+Unemployment.Female+Unemployment.Total+GDP+Birth.rates+Offences+Marriage.Rate,data=clean.df)
clean.lm=lm(Pop.Total~Unemployment.Female+Unemployment.Total+GDP+Birth.rates+Offences+Marriage.Rate,data=clean.df)
clean.lm=lm(Pop.Total~Unemployment.Female+Unemployment.Total+GDP+Birth.rates+Marriage.Rate,data=clean.df)
clean.lm=lm(Pop.Total~Unemployment.Total*Birth.rates+GDP+Marriage.Rate,data=clean.df)

summary(clean.lm)

