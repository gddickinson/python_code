#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#https://docs.python.org/2/library/xml.etree.elementtree.html#module-xml.etree.ElementTree
# Author:      George
#
# Created:     27/06/2017
# Copyright:   (c) George 2017
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import xml.etree.ElementTree as ET

#fileName = r"C:\Google Drive\S2_CHD_George\Tasks\testing\U_S_Geological_Survey_Gap_Analysis_Program_Species_Ranges.xml"
fileName = r"C:\Google Drive\S2_CHD_George\Tasks\testing\test.xml"
saveName = r"C:\Google Drive\S2_CHD_George\Tasks\testing\output.xml"


tree = ET.parse(fileName)
root = tree.getroot()

print (root.tag)

for child in root:
    print (child.tag, child.attrib)

for child in root.iter():
    print (child.tag, child.attrib)

for neighbor in root.iter('neighbor'):
    print (neighbor.attrib)

for country in root.findall('country'):
    rank = country.find('rank').text
    name = country.get('name')
    print (name, rank)

for rank in root.iter('rank'):
    new_rank = int(rank.text) + 1
    rank.text = str(new_rank)
    rank.set('updated', 'yes')

tree.write(saveName)


# Top-level elements
print(root.findall("."))

# All 'neighbor' grand-children of 'country' children of the top-level
# elements
print (root.findall("./country/neighbor"))

# Nodes with name='Singapore' that have a 'year' child
print (root.findall(".//year/..[@name='Singapore']"))

# 'year' nodes that are children of nodes with name='Singapore'
print (root.findall(".//*[@name='Singapore']/year"))

# All 'neighbor' nodes that are the second child of their parent
print (root.findall(".//neighbor[2]"))


##def main():
##    pass
##
##if __name__ == '__main__':
##    main()
