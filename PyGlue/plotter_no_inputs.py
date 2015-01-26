
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
# Set this to True to show the plot
plt.interactive(False)
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
	years_by_term.append(2017) # Just because it's START terms, and National are prob going to be in till 2017
	for i in range(0, len(years_by_term) - 1):
		start_ID = 0
		end_ID = len(df)
		change = False
		try:

			start_ID = get_ID_from_year(years_by_term[i])
			change = True
		except:
			pass

		try:

			end_ID = get_ID_from_year(years_by_term[i + 1])
			change = True
		except:
			pass
		
		if change:
			rect = plt.Rectangle((start_ID,ymin),end_ID - start_ID, ymax - ymin, color = colours_by_term[i])
			ax.add_patch(rect)


ax = df.plot()
draw_parliament_terms()

pd.options.display.mpl_style = 'default'
new_style = {'grid': False}
matplotlib.rc('axes', **new_style)
#plt.show()
plt.savefig('NZDtoUSD.pdf', bbox_inches='tight')

'''
abline(h=1)

years = 12

lo = lowess(compact.df$USD, f = (12*years)/length(compact.df$Date))
lines(index(compact.df$USD),lo$y,lwd=4,col="green")
#dev.off()
'''

arty = test_no_inputs_xml_OUTPUT_XML_arty