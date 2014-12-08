### Load and run an openapi pipeline using conduit

## load the conduit package
library("conduit")

## read a pipeline from the filesystem
mandrought <- loadPipeline(name="mandrought", ref="pipe.xml")

## run the pipeline
runPipeline(mandrought)

## list the resulting files
#list.files(path="pipelines", recursive=TRUE)
