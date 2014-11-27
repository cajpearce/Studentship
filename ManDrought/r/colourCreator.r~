# Creates a colour for P-values - should defo be customised
num.bind = function(v1, low=0, high=1) {
	v1[v1 < 0] = 0
	v1[v1 > 1] = 1
	v1
}

colour.function = function(p.values, v1, midpoint=0.5) {
	indices = log10(1.05 - p.values)/log10(1.05)	
	indices = num.bind(indices) * 0.9
	logical.lower = v1 < midpoint
	cols = ifelse(v1 < midpoint, rgb(0,1,0,alpha=indices),rgb(1,0,0,alpha=indices))
	cols[indices == 0] = rgb(1,1,0,alpha = 0.2)
	cols
}

compact.df$c1 = colour.function(compact.df$p.values,compact.df$percentage)
