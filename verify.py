from urllib.parse import urlparse
import re, os, sys

def get_local_downloaded_file(url):
    o = urlparse(url)
    out = os.path.basename(o.path)
    dir = re.sub(out, '', o.path)
    return dir + out

def verify(listfile):
    err = 0
    outfilename = 'verify_' + listfile
    outf = open('verify_' + listfile, 'w')

    with open(listfile, 'r') as lf:
        for line in lf:
            if line[:4] == 'http':
                url = re.sub(r'    .+', '', line.strip('\n'))
                ldf = '.\\' + get_local_downloaded_file(url)
                if os.path.exists(ldf):
                    if os.path.getsize(ldf) > 0 :
                        outf.write('[OK]    ' + url + '\n')
                    else:
                        print('Empty file:    ' , ldf)
                        outf.write('[ERR_EMPTY_FILE]    ' + url + '\n')
                        err = err + 1
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

    verify(fileinfo)
