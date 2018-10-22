import re
import sys
import time
import os
import shutil

def read_raw_notes(file,dir_out):
    note = ''
    mrn = ''
    primary_time = ''
    alternate_id = ''
    event_code = ''
    event_status = ''
    provider = ''
    last_name = ''
    first_name = ''
    update_time = ''
    text_tag = ''
    flag = 0
    i = 0
    if os.path.exists('log_file.txt'):
        os.remove('log_file.txt')
    log = open('log_file.txt','a')
    with open(file) as f:
        for line in read_line_by_delimited(f):
            try:
                if is_field_line(line):
                    fields = line.split('|')
                    if fields[9] == '1':
                        # ouput the previous report.
                        note = clean_field(note)
                        if(note!=''):
                            header = '|'.join([mrn,primary_time,alternate_id,event_code,event_status,provider,last_name,first_name,update_time,text_tag])
                            context = header + '\n======\n' + note
                            file_prefix = dir_out
                            file_name = 'doc'
                            file_suffix = '.txt'
                            i = print_file(context,i,file_prefix,file_name,file_suffix,log)
                        
                        # re-index the new report.
                        note = clean_quote(fields[13]).rstrip('\n')
                        mrn = clean_field(fields[0])
                        primary_time = clean_field(fields[1])
                        alternate_id = clean_field(fields[2])
                        event_code = clean_field(fields[3])
                        event_status = clean_field(fields[4])
                        provider = clean_field(fields[5])
                        last_name = clean_field(fields[6])
                        first_name = clean_field(fields[7])
                        update_time = clean_field(fields[8])
                        text_tag = clean_field(fields[12])
                    else:
                        note += clean_quote(fields[13]).rstrip('\n')
                else:
                    # it is a chunked note.
                    note += clean_quote(line)

            except:
                log.write('ERROR MRN: ' + mrn)
                log.write('ERROR TIME: ' + time)
                log.write('ERROR LINE: ' + line)
                log.write('Unexpected error:' + sys.exc_info()[0])
                flag = 1
    log.close()
    return flag

def print_file(context,i,file_prefix,file_name,file_suffix,log_file_handle,file_per_fold = 10000):
    working_dir = ''
    try:
        if(i % file_per_fold == 0):
            # make a directory per 10000 files.
            print(str(i) + ' docs created...',flush=True)
            working_dir = file_prefix + '/' + file_name + '_' + str(i)
            if not os.path.exists(working_dir):
                os.makedirs(working_dir)
        else:
            working_dir = file_prefix + '/' + file_name + '_' + str(i-(i%file_per_fold))

        file_output = working_dir + '/' + file_name + '_' + str(i) + file_suffix     
        f = open(file_output,'w')
        f.write(context)
        f.close()
    except:
        log_file_handle.write('Unexpected error:' + sys.exc_info()[0])
    return i + 1


# whether it is a field line or note line.                
def is_field_line(line):
    fields = line.split('|')
    if(len(fields) == 14):
        return True
    else:
        return False

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
    file = 'crown_472.txt'
    dir_out = 'cleaned_out'
    if os.path.exists(dir_out):
            try:
                shutil.rmtree(dir_out)
            except OSError as e:
                print (e.filename + '\n' + e.strerror)
    os.makedirs(dir_out)        
    base_time = time.clock()
    flag = read_raw_notes(file,dir_out)
    consumed = time.clock() - base_time
    if flag == 0:
        print('Note parses success.')
        print('TIME:' + str(consumed))
    else:
        print('Some errors occur during the parse.')
