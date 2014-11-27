### Load and run an openapi pipeline using conduit

## load the conduit package
library("conduit")

## read a pipeline from the filesystem
helloworld <- loadPipeline(name="helloworld", ref="p1.xml")

## run the pipeline
runPipeline(helloworld)

## list the resulting files
list.files(path="pipelines", recursive=TRUE)

## see the resulting PDF
system("evince pipelines/helloworld/modules/m2/Rplots.pdf &")
