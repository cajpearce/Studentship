# Add a column for the percentage of females by total
compact.df$percentage = compact.df$Female/compact.df$Total

# Perform a Proportion test on all the 
# doing prop.test on a vector just returns proportions; need to do it individually to get p-values
pt.pvalues = function(v1, v2) {
  count = numeric(0)
  for (i in 1:length(v1)) {
    p.val = prop.test(v1[i],v2[i])$p.value
    count = c(count, p.val)
  }
  count
}

compact.df = cbind(compact.df,p.values = pt.pvalues(compact.df$Female,compact.df$Total))

