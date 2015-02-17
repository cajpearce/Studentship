import wikimarkup, urllib2, re
import pandas as pd
import numpy as np
from pyquery import PyQuery
from matplotlib import colors as cl

fromurl = "http://en.wikipedia.org/wiki/New_Zealand_Parliament"


def get_wiki_raw(url):
	text_url = re.sub("wiki/","w/index.php?title=",url) + "&action=edit"
	raw_html = urllib2.urlopen(text_url).read()
	text = raw_html[re.search("<textarea.*?>",raw_html).end():]
	text = text[:re.search("</textarea>",text).start()]
	return text
	

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
