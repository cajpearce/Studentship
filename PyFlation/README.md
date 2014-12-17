Reflections on PyFlation:

Original was Inflation. Converted to Python. Essentially the same.

<b>Preface:</b>

<b>Module 1 - inflation.py:</b>

Download spreadsheet from the reserve bank, take the right worksheet, grab the
USD information.
	
Use xlrd to read the excel file, use pandas to store the information as a 
dataset. pandas attempts a pythonic representation of data the way R stores data

<b>Module 2 - htmlscraper.py:</b>
	
Read the editable version of text from a wikipedia page and grab a table from it.

A lot of these functions can be used more generally as separate modules, but i 
prefer the hybrid approach.
	
In the htmlscraper.py is also the processing to assign colours to different 
parties: National gets blue, Labour gets red, old parties get green. In all 
effectiveness the old parties are redundant with the USD information because the
dataset only goes back to the 1970s, but it promotes a more generic feel and can
be reused this way.

Uses wikimarkup and pyquery to grab a table from a wikipedia page.

Done very differently in R: in R I grabbed it directly from the html but for 
python I lazily copied some code from a stackoverflow page. Luckily there is 
already a wikimarkup library so took a lot of the work out of it.
But was definitely easier in R.

<b>Module 3 - plotter.py:</b>

The process is essentially the same as in R, except with a few edits. In python 
I decided to draw the colour boxes (for different Parliament terms) literally as
they started/ended. in R this was done differently - it was done at the start of
each term, not at the start of each government change.

The code for R is a lot shorter, for essentially the same results. Plus I 
managed to fit in a lowess fitted line in R. In R the plot is made in under half
the lines of code, and makes so much more sense.

Conclusion? Python sucks for this sort of stuff.


<b><u>Code follow-through:</u></b>

<b>Module 1 - inflation.py:</b>

```
rb_socket = urllib2.urlopen('http://www.rbnz.govt.nz/statistics/key_graphs/graphdata.xls')
data = pd.io.excel.read_excel(rb_socket, 7, skiprows=4)
```
Read the data into a dataframe (data) from the remote excel file

```
# Grabs the dates
dates = data['DATE']

# Replaces 'M' with '-' and makes a date object out of it
new_dates = pd.DataFrame(map(lambda x: re.sub("M","-",x), dates))
new_dates = pd.DatetimeIndex(new_dates[0]).to_period('M')
```
Converts dates to an actual 'date' format

```
df = pd.DataFrame(data['R$USD'],index=new_dates)
```
Picks the USD and date information and make a new dataframe


<b>Module 2 - htmlscraper.py:</b>

```
fromurl = "http://en.wikipedia.org/wiki/New_Zealand_Parliament"


def get_wiki_raw(url):
	text_url = re.sub("wiki/","w/index.php?title=",url) + "&action=edit"
	raw_html = urllib2.urlopen(text_url).read()
	text = raw_html[re.search("<textarea.*?>",raw_html).end():]
	text = text[:re.search("</textarea>",text).start()]
	return text

```
Convert a wikipedia URL to the editable URL, then takes the markup text from the
html

```
def get_tables(url):
    html = PyQuery(wikimarkup.parse(get_wiki_raw(url)))
    frames = pd.DataFrame()
    for table in html('table'):
        data = [[x.text.strip() for x in row]
                for row in table.getchildren()]
        df = pd.DataFrame(data[1:], columns=data[0])
        if np.prod(df.shape) > np.prod(frames.shape):
		frames = df
    return frames



nzp = get_tables(fromurl)
```
Gets a wikipedia table. Taken from http://stackoverflow.com/questions/15724034/how-to-convert-wikipedia-wikitable-to-python-pandas-dataframe

```
def rename_col(df, index, name):
	cols = list(df.columns)
	cols[index] = name
	df.columns = cols



rename_col(nzp,1,"Year")



def get_years(yearList):
	x = []
	bad_indexes = []
	count = 0
	for l in yearList:
		if type(l) is str:
			x.append(re.search('[0-9]{4}',l).group(0))
		else:
			x.append(None)
			bad_indexes.append(count)
		count += 1
	return x, bad_indexes


nzp['Year'], baddies = get_years(nzp['Year'])

nzp.drop(baddies,inplace=True)
```
Renames the year column to "Year" for easy access, then gets the actual numeric
years from the weird formatting that wikipedia uses. Simultaneously drops NA
rows.

```
def get_original_table_names(tableList):
	x = []
	for l in tableList:
		if type(l) is str:
			s = re.findall('[^\[\]|]+',l)
			x.append(s[len(s) - 1])
		else:
			x.append(None)
	return x

nzp['Government'] = get_original_table_names(nzp['Government'])
nzp['Term'] = get_original_table_names(nzp['Term'])
```

Cleans up the other columns (required due to the crap wikipedia formatting) to
only show the important information.

```
def pad_names(pl):
	padList = list(pl)
	current = ""
	for i in range(0,len(padList)):
		if padList[i] is None:
			padList[i] = current
		elif current != padList[i]:
			current = padList[i]
	return padList

nzp['Government'] = pad_names(nzp['Government'])
```
Originally the Government name was only stored when they first came into power,
successive terms were counted as NA. this just pads the data so that subsequent
terms are consequentially named the same as when the Gov. first came into power.

```
# may need to change color definitions
blue =  (0.25,0.25,1,0.2)
red =   (1,0.25,0.25,0.2)
green = (0.25,1,0.25,0.2)

def colour_function(party):
	party = list(party)
	other = []
	for p in party:
		if re.search("Labour",p) is not None:
			other.append(red)
		elif re.search("National",p) is not None:
			other.append(blue)
		else:
			other.append(green)
	return other

colours = colour_function(nzp['Government'])
```
Creates a colour vector, assigning a colour to different governments. Blue is
national, red is labour, green is other. Can easily be changed to take all
parties into account (ie green split into yellow, orange,etc.)


<b>Module 3 - plotter.py:</b>
```
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
```
Get the starting years for terms. Needed for drawing colour rectangles
```
def get_ID_from_year(year):
	global df
	years = list(df.index.year)
	return years.index(year)
```
Since python is retarded, it plots the x axis by observation. since there are
roughly 500 USD observations, the x axis ranges from 0 to 500. As such I need
the above helper function just to get the year (or its first observation) index
in relation to the observations. R is so much easier.

```
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
```
draws the rectangles. That's all this does. Look at R and tell me it doesn't
look easier.

Regardless, it works by taking the terms, getting the xmin and xmax, and making
sure it plots within those regions. It works, but the logic is unwieldy for such
a simple task.

```
ax = df.plot()
draw_parliament_terms()

pd.options.display.mpl_style = 'default'
new_style = {'grid': False}
matplotlib.rc('axes', **new_style)
#plt.show()
plt.savefig('NZDtoUSD.pdf', bbox_inches='tight')
```
df.plot() actually plots the USD information (yahee!) which is followed by
drawing the boxes that represent parliament terms. The rest is style information
and saving it to a pdf.

:)
