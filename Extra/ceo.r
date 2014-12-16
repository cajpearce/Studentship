ceo.df = read.csv("ceo.CSV")
ceo.df = ceo.df[-1]
ceo.df = ceo.df[-3]
ceo.lm = lm(SCORE~.,data=ceo.df)
summary(ceo.lm)

# Will be good later
