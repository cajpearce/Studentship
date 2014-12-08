# Cleans up a dataframe by removing unnecessary columns with useless input
########## Module

def remove_1D_rows(df):
	df = df.copy()
	for col in df.columns:
		column = map(lambda x: str(x), df[col])
		column = set(column)
		if len(column) == 1:
			del df[col]
	return df


compact.df = remove_1D_rows(df)
