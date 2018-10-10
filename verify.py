from urllib.parse import urlparse
import re, os, sys

def get_local_downloaded_file(url):
    o = urlparse(url)
    out = os.path.basename(o.path)
    dir = re.sub(out, '', o.path)
    return dir + out

def import_dict(dictpath):
    fileinfo_dic = {}
    with open(dictpath, 'r') as dict:
        for line in dict:
            l = line.split()
            fileinfo_dic[l[0]] = l[3]
    return fileinfo_dic

def convert_size_byte(size_str):
    if size_str[-1] == 'K':
        num = float(size_str[:-1])
        size_in_byte = num * 1024
    elif size_str[-1] == 'M':
        num = float(size_str[:-1])
        size_in_byte = num * 1024 * 1024
    elif size_str [-1] == 'G':
        num = float(size_str[:-1])
        size_in_byte = num * 1024  * 1024 * 1024
    else:
        num = float(size_str)
        size_in_byte = num
    return size_in_byte

def verify(listfile, fileinfo_dic):
    err = 0
    outfilename = 'verify_' + listfile
    outf = open('verify_' + listfile, 'w')

    with open(listfile, 'r') as lf:
        for line in lf:
            if line[:4] == 'http':
                url = re.sub(r'    .+', '', line.strip('\n'))
                ldf = '.' + get_local_downloaded_file(url)
                if os.path.exists(ldf):
                    #check size
                    actual_size = os.path.getsize(ldf) # in byte
                    correct_size = convert_size_byte(fileinfo_dic[url]) # in byte
                    if actual_size == 0 and correct_size != 0:
                        print('Empty file:    ' , ldf)
                        print('\tactual:', actual_size, '; correct:', correct_size, ';dif:', abs(actual_size - correct_size) )
                        outf.write('[ERR_EMPTY_FILE]    ' + url + '\n')
                        err = err + 1
                    elif correct_size < 1024: #byte level error: 10b
                        if abs(actual_size - correct_size) > 10:
                            print('Wrong size(byte):    ' , ldf)
                            print('\tactual:', actual_size, '; correct:', correct_size, ';dif:', abs(actual_size - correct_size) )
                            outf.write('[ERR_WRONG_SIZE]    ' + url + '\n')
                            err = err + 1
                    elif correct_size >= 1024 and correct_size < 1048576: #kb level error: 1k
                        if abs(actual_size - correct_size) > 1024:
                            print('Wrong size(kb):    ' , ldf)
                            print('\tactual:', actual_size, '; correct:', correct_size, ';dif:', abs(actual_size - correct_size) )
                            outf.write('[ERR_WRONG_SIZE]    ' + url + '\n')
                            err = err + 1
                    elif correct_size >= 1048576 and correct_size < 1073741824: #mb level error: 1m
                        if abs(actual_size - correct_size) > 1048576:
                            print('Wrong size(mb):    ' , ldf)
                            print('\tactual:', actual_size, '; correct:', correct_size, ';dif:', abs(actual_size - correct_size) )
                            outf.write('[ERR_WRONG_SIZE]    ' + url + '\n')
                            err = err + 1
                    elif correct_size >= 1073741824: #gb level error: 0.1g
                        if abs(actual_size - correct_size) > 107374182:
                            print('Wrong size(gb):    ' , ldf)
                            print('\tactual:', actual_size, '; correct:', correct_size, ';dif:', abs(actual_size - correct_size) )
                            outf.write('[ERR_WRONG_SIZE]    ' + url + '\n')
                            err = err + 1
                    else:
                        pass
                    outf.write('[OK]    ' + url + '\n')
                else:
                    print('Missing:    ' , ldf)
                    outf.write('[ERR_FILE_MISSING]    ' + url + '\n')
                    err = err + 1
            else:
                pass
    outf.close()
    if err == 0:
        os.rename(outfilename, 'OK_'+outfilename)
    else:
        os.rename(outfilename, 'ERR_'+outfilename)


if __name__ == "__main__":
    #argument: url list only
    ##########################################


    fileinfo = str(sys.argv[1])
    sizeinfolist = str(sys.argv[2])
    size_dict = import_dict(sizeinfolist)

    verify(fileinfo, size_dict)
    
