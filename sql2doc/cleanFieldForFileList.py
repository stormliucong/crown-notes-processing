import re
import sys
import time
import os
import shutil

def html2clean(input,output,log):
    input = input.strip('\n')
    output = output.strip('\n')
    p = re.compile('.*doc_(.+?)\\.html')
    m = re.match(p, input)
    flag = 0
    if m:
        try:
            docId = m.group(0)
            o = open(output,'w+')
            note = ''
            with open(input) as f:
                for line in f.readlines():
                    if is_field_line(line):
                        o.write(line)
                    elif is_seperate_line(line):
                        o.write(line)
                    else:
                        note += line

                note = clean_non_ascii(note)
                note = add_linebreak(note)
                note = clean_html(note)
                note = clean_space(note)
            o.write(note)
            o.close()

        except:
            l = open(log,'a+')
            l.write('ERROR DOC: ' + docId)
            l.write('Unexpected error:' + sys.exc_info()[0])
            l.close()    
            flag = 1

    return flag

# whether it is a field line or note line.                
def is_field_line(line):
    fields = line.split('|')
    if(len(fields) == 14):
        return True
    else:
        return False

def is_seperate_line(line):
    return line=='======'

# read line by customized delimiter.
def read_line_by_delimited(file, delimiter='\n', bufsize=4096):
    buf = ''
    while True:
        newbuf = file.read(bufsize)
        if not newbuf:
            yield buf # using yield to avoid load everything in RAM. Generator
            return
        buf += newbuf
        lines = buf.split(delimiter)
        for line in lines[:-1]:
            yield line + delimiter
        buf = lines[-1]

# clean field
def clean_field(field):
    field = clean_quote(field)
    field = clean_non_ascii(field)
    field = add_linebreak(field)
    field = clean_html(field)
    field = clean_space(field)
    return field

# replace tag <p>
def add_linebreak(string):
    cleanr = re.compile('<p>')
    string = re.sub(cleanr,'\n',string)
    cleanr = re.compile('<br>')
    string = re.sub(cleanr,'\n',string)
    return string

# clean html tag
def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    clean_text = re.sub(cleanr,' ',raw_html)
    return clean_text

# clean  spaces and  in a line
def clean_space(string):
    cleanr = re.compile(' +')
    clean_text = re.sub(cleanr,' ',string)
    return clean_text

# clean non ascii char
def clean_non_ascii(string):
    cleanr = re.compile('[^\x00-\x7f]')
    string = re.sub(cleanr,'',string)
    cleanr = re.compile('&nbsp;')
    string = re.sub(cleanr,'',string)
    return string

def clean_quote(string):
    cleanr = re.compile('^\"')
    string = re.sub(cleanr,'',string)
    cleanr = re.compile('\"$')
    string = re.sub(cleanr,'',string)
    return string


if __name__ == '__main__':
    file_list = sys.argv[1]     
    base_time = time.clock()
    with open(file_list,'r+') as file_list:
        for line in file_list.readlines():
            input = line
            cleanr = re.compile('\\.html')
            output = re.sub(cleanr,'.txt',input)
            print(output)
            log = 'log.txt'
            flag = html2clean(input,output,log)

    consumed = time.clock() - base_time
    file_list.close()
    if flag == 0:
        print('Note parses success.')
        print('TIME:' + str(consumed))
    else:
        print('Some errors occur during the parse.')
