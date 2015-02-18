### Load and run an openapi pipeline using conduit

## load the conduit package
library("conduit")

## read a pipeline from the filesystem
tides <- loadPipeline(name="tides", ref="pipe.xml")

## run the pipeline
runPipeline(tides)

## list the resulting files
#list.files(path="pipelines", recursive=TRUE)
