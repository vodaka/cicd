import xml.etree.ElementTree as ET

tree = ET.parse('template.xml')
root = tree.getroot()
# print root.tag

for child in root.iter('spec'):
    print child.tag, child.text
    child.text = 'H/2 * * * *'
    print (child.text)

tree.write('aaa.xml')

# for spec in root.findall('spec'):
#     print spec.tag, spec.text
