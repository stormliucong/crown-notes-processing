#!/usr/bin/env python
# coding: utf-8

# In[120]:


from lxml import etree
import re
import sys
import os
import time


# In[91]:


def cytoband2medlee(cytoband,medlee=None):
    """
    cytoband is downloaded from
    http://hgdownload.cse.ucsc.edu/goldenpath/hg38/database/cytoBand.txt.gz 
    """
    if not medlee:
        medlee = re.sub('(^.+?\.)txt$','\g<1>medlee.txt',cytoband)
    id = ''
    label = ''
    synonym = ''
    i = 0
    syn_dict = {}
    with open(cytoband,'r+') as c:
        for line in c.readlines():
            if not re.match('^#.+?',line):
                cols = line.strip('\n').split('\t')
                chr = cols[0]
                m = re.match('^chr(1?[1-9]|2[0-2]|X|Y|10)$',chr)
                if m :
                    chr_num = m.group(1)
                    band = cols[3]
                    id = chr_num
                    label = id
                    key = label
                    if key not in syn_dict:
                        syn_dict[key] = set()
                    syn_dict[key].add(band)
    
    with open(medlee,'w+') as o:
        for key in syn_dict:
            o.write(key+'q' + '\t' + key+'q' + '\t' + key+'q' + '\n')
            o.write(key+'p' + '\t' + key+'p' + '\t' + key+'p' + '\n')
            i += 1
            for value1 in syn_dict[key]:
                o.write(key+value1 + '\t' + key+value1 + '\t' + key+value1 + '\n')
                for value2 in syn_dict[key]:
                    if value1 != value2:
                        o.write(key+value1+'-'+value2 + '\t' + key+value1+'-'+value2 + '\t' + key+value1+'-'+value2 + '\n')
    print('{0} Ids processed!'.format(i))
    return None


# In[32]:


def hgnc2medlee(hgnc,medlee=None):
    '''
    hgnc is downloaded from
    https://biomart.genenames.org/martform/#!/default/HGNC?datasets=hgnc_gene_mart
    '''
    if not medlee:
        medlee = re.sub('(^.+?\.)txt$','\g<1>medlee.txt',hgnc)
    id = ''
    label = ''
    synonym = ''
    i = 0
    syn_dict = {}
    with open(hgnc,'r+') as h:
        for line in h.readlines():
            if not re.match('^#.+?',line):
                cols = line.strip('\n').split('\t')
                id = cols[0]
                label = cols[2].strip()
                if label:
                    key = id + '\t' + label
                    if key not in syn_dict:
                        syn_dict[key] = set()
                        syn_dict[key].add(label)
                        for i in [3,4,5,6,7,8]:
                            synonym = cols[i].strip()
                            if synonym and synonym != 'entry withdrawn':
                                syn_dict[key].add(synonym)

    with open(medlee,'r+') as o:
        for key in syn_dict:
            i += 1
            for value in syn_dict[key]:            
                o.write(key + '\t' + value + '\n')
    print('{0} Ids processed!'.format(i))
    return None


# In[97]:


def owl2medlee_for_hpo(owl,medlee=None):
    '''
    hpo is downloaded from
    http://purl.obolibrary.org/obo/hp.owl
    '''
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
                    for ele4 in ele1.findall('oboInOwl:hasExactSynonym',root.nsmap):
                        synonym = ele4.text
                        o.write(id + '\t' + label + '\t' + synonym + '\n')
                else:
                    next
    print('{0} Ids processed!'.format(i))
    return None


# In[104]:


def owl2medlee_for_ordo(owl,medlee=None):
    '''
    orphanet is downloaded from
    https://www.ebi.ac.uk/ols/ontologies/ordo
    '''
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


# In[105]:


def trim_included(string):
    '''
    remove the INCLUDE text in OMIM
    '''
    string = re.sub(', INCLUDED$','',string)
    return(string)


# In[115]:


def mimTitles2medlee(mimTitles,medlee=None):
    '''
    omim is downloaded from 
    https://www.omim.org/downloads/
    '''
    medlee = re.sub('(^.+?\.)txt$','\g<1>medlee.txt',mimTitles)
    id = ''
    label = ''
    synonym = ''
    i = 0
    with open(medlee,'w+') as o:
        omim = open(mimTitles,'r+')
        '''
        http://omim.org/help/faq#1_3
        '''
        for line in omim.readlines():
            if not re.match('^#.+?',line):
                cols = line.strip('\n').split('\t')
                prefix = cols[0]
                if prefix in ['Number Sign','Percent','NULL']:
                    id = cols[1]
                    i += 1
                    labels = cols[2].split(';')

                    label = trim_included(labels[0])

                    o.write(id + '\t' + label + '\t' + label + '\n')
                    if len(labels) > 1:
                        label_symbol = trim_included(labels[1])
                        o.write(id + '\t' + label + '\t' + label_symbol + '\n')

                    synonym1 = cols[3]
                    synonym2 = cols[4]
                    for syn in [synonym1,synonym2]:
                        inds = syn.split(';;')
                        for ind in inds:
                            if ind:

                                ts = ind.split(';')
                                title = trim_included(ts[0])
                                o.write(id + '\t' + label + '\t' + title + '\n')
                                if len(ts) > 1:
                                    symbol = trim_included(ts[1])
                                    o.write(id + '\t' + label + '\t' + symbol + '\n')
        omim.close()
    print('{0} Ids processed!'.format(i))
    return None          


# In[123]:


def file_to_lower(input):
    '''
    change to lower case required by medlee
    '''
    output = re.sub('(^.+?\.)txt$','\g<1>lowercase.txt',input)
    with open(output,'w+') as o:
        i = open(input,'r+')
        for line in i.readlines():
            o.write(line.lower())
        i.close()
    return None


# In[98]:


owl2medlee_for_hpo('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/hp.owl')


# In[108]:


owl2medlee_for_ordo('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/ordo.owl')


# In[116]:


mimTitles2medlee('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/mimTitles.txt')


# In[117]:


hgnc2medlee('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/hgnc.txt')


# In[118]:


cytoband2medlee('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/cytoBand.txt')


# In[127]:


for (dirpath, dirnames, filenames) in os.walk('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/'):
    for filename in filenames:
        if filename.endswith('.medlee.txt'):
            abspath = os.path.abspath(filename)
            print(abspath)
            file_to_lower(abspath)


# In[ ]:


if __name__ == '__main__':
    owl2medlee_for_hpo(sys.argv[1])
    owl2medlee_for_ordo(sys.argv[2])
    mimTitles2medlee(sys.argv[3])
    hgnc2medlee(sys.argv[4])
    cytoband2medlee(sys.argv[5])
    time.sleep(60)
    for (dirpath, dirnames, filenames) in os.walk('/Users/cl3720/Projects/crown-notes-processing/dictionary-generator/'):
        for filename in filenames:
            if filename.endswith('.medlee.txt'):
                abspath = os.path.abspath(filename)
                print(abspath)
                file_to_lower(abspath)

