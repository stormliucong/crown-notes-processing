
# coding: utf-8

# In[1]:


from lxml import etree
import re
import sys


# In[2]:


def owl2medlee_for_hpo(owl,medlee=None):
    
    if not medlee:
        medlee = re.sub('(^.+?\.)owl$','\g<1>medlee.txt',owl)

    tree = etree.parse(owl)
    root = tree.getroot()
    id = ''
    label = ''
    synonym = ''
    i = 0
    with open(medlee,'w+') as o:
        for ele1 in root.findall('owl:Class', root.nsmap):
            for ele2 in ele1.findall('oboInOwl:id',root.nsmap):
                m = re.match('^(HP:\d+)$', ele2.text)
                if m:
                    id = ele2.text
                    i += 1
                    for ele3 in ele1.findall('rdfs:label', root.nsmap):
                        label = ele3.text
                        o.write(id + '\t' + label + '\t' + label + '\n')
                    for ele4 in ele1.findall('efo:alternative_term',root.nsmap):
                        synonym = ele4.text
                        o.write(id + '\t' + label + '\t' + synonym + '\n')
                else:
                    next
    print('{0} Ids processed!'.format(i))
    return None


# In[10]:


def owl2medlee_for_ordo(owl,medlee=None):
    medlee = re.sub('(^.+?\.)owl$','\g<1>medlee.txt',owl)
    tree = etree.parse(owl)
    root = tree.getroot()
    id = ''
    label = ''
    synonym = ''
    i = 0
    with open(medlee,'w+') as o:
        for ele1 in root.findall('owl:Class', root.nsmap):
            for ele2 in ele1.findall('skos:notation',root.nsmap):
                m = re.match('^(ORPHA:\d+)$',ele2.text)
                if m :
                    id = ele2.text
                    i +=1
                    for ele3 in ele1.findall('rdfs:label',root.nsmap):
                        label = ele3.text
                        o.write(id + '\t' + label + '\t' + label + '\n')
                    for ele4 in ele1.findall('efo:alternative_term',root.nsmap):
                        synonym = ele4.text
                        o.write(id + '\t' + label + '\t' + synonym + '\n')
                else:
                    next
    print('{0} Ids processed!'.format(i))
    return None          


# In[ ]:


if __name__ == '__main__':
#     owl2medlee_for_hpo(sys.argv[0])
    owl2medlee_for_ordo(sys.argv[0])

