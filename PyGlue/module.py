try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

tree = ET.ElementTree(file="test.xml")
root = tree.getroot()


for elem in tree.iter():
	print elem.tag, elem.attrib

#{http://www.openapi.org/2014/}platform {'name': 'python'}
#{http://www.openapi.org/2014/}description {}
#{http://www.openapi.org/2014/}output {'type': 'internal', 'name': 'df'}
#{http://www.openapi.org/2014/}source {'ref': 'inflation.py'}

