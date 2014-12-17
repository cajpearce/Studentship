Reflections on PyFlation:

Original was Inflation. Converted to Python. Essentially the same.

Preface:

Module 1 - inflation.py:
	download spreadsheet from the reserve bank, take the right worksheet, 
	grab the USD information.
	
	Use xlrd to read the excel file, use pandas to store the information as
	a dataset. pandas attempts a pythonic representation of data the way
	R stores data

Module 2 - htmlscraper.py:
	read the editable version of text from a wikipedia page and grab a table
	from that.

	a lot of these functions can be used more generally as separate modules,
	but i prefer the hybrid approach.
	
	in the htmlscraper.py is also the processing to assign colours to
	different parties: National gets blue, Labour gets red, old parties get 
	green. In all effectiveness the old parties are redundant with the
	USD information because the dataset only goes back to the 1970s, but
	it promotes a more generic feel and can be reused this way.

	uses wikimarkup and pyquery to grab a table from a wikipedia page.

	Done very differently in R: in R I grabbed it directly from the html
	but for python I lazily copied some code from a stackoverflow page.
	Luckily there is already a wikimarkup library so took a lot of the work
	out of it. But was definitely easier in R.

Module 3 - plotter.py:
	The process is essentially the same as in R, except with a few edits.
	In python I decided to draw the colour boxes (for different Parliament
	terms) literally as they started/ended. in R this was done differently -
	it was done at the start of each term, not at the start of each govt.
	change.

	The code for R is a lot shorter, for essentially the same results. Plus
	I managed to fit in a lowess fitted line in R. In R the plot is made in
	under half the lines of code, and makes so much more sense.

	Conclusion? Python sucks for this sort of stuff.


Code follow-through:

Module 1 - inflation.py:

```
new_dates = pd.DataFrame(map(lambda x: re.sub("M","-",x), dates))
new_dates = pd.DatetimeIndex(new_dates[0]).to_period('M')
```
