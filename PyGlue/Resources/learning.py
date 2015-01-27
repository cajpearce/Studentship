################################################################################
# Learning how to use lxml
################################################################################
# :)
################################################################################

# prints out the XML
print etree.tostring(root, pretty_print=True)


# prints out all the sub-element tags
for child in root:
	print child.tag

# prints out whether the root element is an element
print etree.iselement(root)

# prints if the root has sub elements
if len(root):
	print("The root element has children")


# testing out the abilities to detect the parent
print root is root[0].getparent()

# testing out navigation
print root[0] is root[1].getprevious() and root[1] is root[0].getnext()

# prints out root tags (stuff like version)
print "ROOT KEYS: " +str(root.keys())

# ALTERNATIVE
attributes_of_root = root.attrib

print "DIRECT KEYS: " + str(attributes_of_root)

# prints out the version hopefully
print "VERSION: " + str(root.get(root.keys()[0]))


# Testing iterators
for element in root.iter():
	print("%s - %s" % (element.tag, element.text))

# Specific iterators
for element in root.iter(namespace + "platform"):
	# NOTE THAT YOU HAVE TO PREFACE THE NAMESPACE AT THE MOMENT...
	print("%s - %s" % (element.tag, element.text))

print
print
print
print
# Appending a comment!
#root.append(etree.Comment("Hi there!"))

