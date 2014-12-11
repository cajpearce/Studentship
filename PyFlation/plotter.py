import matplotlib
import matplotlib.pyplot as plt
plt.interactive(True)

ax = df.plot()


# I need to convert years into the ID of the observation

def year_start_terms(item_list):
	global nzp
	
	govt = list(nzp['Government'])
	years = list(item_list)

	first_govt = 0
	
	ret_list = [years[first_govt]]
	
	for term in range(1,len(govt)):
		if govt[term] is not govt[first_govt]:
			ret_list.append(years[term])
			first_govt = term
	return ret_list


def get_ID_from_year(year):
	global df
	years = list(df.index.year)
	return years.index(year)


def draw_parliament_terms():
	global ax,df,colours,nzp
	
	ymin = ax.axis()[2]
	ymax = ax.axis()[3]

	colours_by_term = year_start_terms(colours)
	years_by_term = map(int, year_start_terms(nzp['Year']))
	
	for i in range(0, len(years_by_term) - 1):
		start_year = 0
		end_year = len(df)
		try:
			start_year = get_ID_from_year(years_by_term[i])
		except:
			pass

		try:
			end_year = get_ID_from_year(years_by_term[i + 1])
		except:
			pass

		if start_year != 0 and end_year != len(df):
			rect = plt.Rectangle((start_year,ymin),end_year - start_year, ymax - ymin, color = colours_by_term[i])
			ax.add_patch(rect)

draw_parliament_terms()

'''
abline(h=1)

years = 12

lo = lowess(compact.df$USD, f = (12*years)/length(compact.df$Date))
lines(index(compact.df$USD),lo$y,lwd=4,col="green")
#dev.off()
'''
