### Load and run an openapi pipeline using conduit

## load the conduit package
library("conduit")

## read a pipeline from the filesystem
inflation <- loadPipeline(name="inflation", ref="pipe.xml")

## run the pipeline
runPipeline(inflation)

## list the resulting files
#list.files(path="pipelines", recursive=TRUE)
