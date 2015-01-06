### Load and run an openapi pipeline using conduit

## load the conduit package
library("conduit")

#inflation <- loadPipeline(name="inflation", ref="pipe.xml")

#runPipeline(inflation)


df.out = moduleOutput(name="df",type="internal")
df.in = moduleInput(name="df",  type="internal")

nzp.out = moduleOutput(name="nzp",type="internal")
nzp.in = moduleInput(name="nzp",  type="internal")

fiscal.r = moduleSource(ref="fiscal.r")
htmlscraper.r = moduleSource(ref="htmlscraper.r")
plotter.r = moduleSource(ref="plotter.r")

fiscal.CSV = module(name="fiscal","R",outputs=list(df.out),sources=list(fiscal.r))
scraper = module(name="scraper","R",outputs=list(nzp.out),sources=list(htmlscraper.r))
plotter = module(name="plotter","R",inputs=list(df.in,nzp.in),sources=list(plotter.r))

p1 = pipe("fiscal","df","plotter","df")
p2 = pipe("scraper","nzp","plotter","nzp")

finished = pipeline("itsthefinalpipeline",modules=list(fiscal.CSV,scraper,plotter),
		pipes=list(p1,p2))

