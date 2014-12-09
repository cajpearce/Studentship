# Creates a colour for P-values - should defo be customised
library(scales)


# would multiplying the P-value by (0.5 - percentage) * 2 be more relevant?

num.bind = function(v1, low=0, high=1) {
	v1[v1 < 0] = 0
	v1[v1 > 1] = 1
	v1
}

colour.function = function(p.values, v1, midpoint=0.5, cutoff=0.05, offset = 0.01) {
	indices = log10(1 + cutoff + offset - p.values)/log10(1 + cutoff + offset)	
	indices = num.bind(indices)
	cols = ifelse(v1 < midpoint, rgb(0,1,0,alpha=indices),rgb(1,0,0,alpha=indices))
	cols[p.values > cutoff] = rgb(1,1,0,alpha = 0.2)
	cols
}

compact.df$c1 = colour.function(compact.df$p.values,compact.df$percentage)
