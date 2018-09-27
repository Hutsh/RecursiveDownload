import re
from hurry.filesize import size

def convert_size(size_str):
    if size_str[-1] == 'K':
        num = float(size_str[:-1])
        size_in_mb = num / 1024
    elif size_str[-1] == 'M':
        num = float(size_str[:-1])
        size_in_mb = num
    elif size_str [-1] == 'G':
        num = float(size_str[:-1])
        size_in_mb = num * 1024
    else:
        num = float(size_str)
        size_in_mb = num / 1024 / 1024

    size_in_b = size_in_mb * 1024 * 1024
    return size_in_mb


def cal_size(file, year, month):

    url = '*****://*******.****.****.***/***/*****/****/***/*******/**********/*****/************.***.**	06-Mar-2018 16:55 124K'
    if month < 10:
        month = '0'+str(month)
    else:
        month = str(month)
    pr = r'.+' + str(year) + r'_' + month + r'.+'
    pattern = re.compile(pr)

    t_size = 0

    with open(file, 'r') as f:
        for line in f:
            if pattern.match(line.strip('\n')):
                size_str = line.split()[3]
                b = convert_size(size_str)
                t_size = t_size + b
    return(t_size/1024)

def sepeate_by_size(file, sepSize=10000): #sepSize:mb
    rangeStart = '2017_06'
    rangeEnd = '2018_09'
    curMonth = rangeStart
    pr = r'.+' + curMonth + r'.+'
    pattern = re.compile(pr)
    sizeCount = 0
    curOutFileIndex = 1
    curOutFileName = 'sep_'+ curMonth + '_' + str(curOutFileIndex) + '.txt'
    outf = open(curOutFileName, 'w')

    with open(file, 'r') as f:
        for line in f:
            if line[:4] != 'http':
                print(line)
                break

            if pattern.match(line.strip('\n')):
                size_str = line.split()[3]
                url = line.split()[0]
                mb = convert_size(size_str)
                sizeCount = sizeCount + mb
                if sizeCount >=sepSize:
                    outf.write('Total Size:' + str(sizeCount) + 'MB\n')
                    outf.close()
                    sizeCount = 0
                    curOutFileIndex = curOutFileIndex + 1
                    curOutFileName = 'sep_'+ curMonth + '_' + str(curOutFileIndex) + '.txt'
                    outf = open(curOutFileName, 'w')
                    outf.write(url+'\n')
                else:
                    outf.write(url+'\n')
                    pass
            else:
                curMonth = month_add(curMonth)
                pr = r'.+' + curMonth + r'.+'
                pattern = re.compile(pr)

                outf.write('Total Size:' + str(sizeCount) + 'MB\n')
                outf.close()

                sizeCount = 0
                curOutFileIndex = 1
                curOutFileName = 'sep_'+ curMonth + '_' + str(curOutFileIndex) + '.txt'

                outf = open(curOutFileName, 'w')
                size_str = line.split()[3]
                url = line.split()[0]
                mb = convert_size(size_str)
                sizeCount = sizeCount + mb
                outf.write(url+'\n')
    outf.write('Total Size:' + str(sizeCount) + 'MB\n')
    outf.close()

def month_add(month):
    mdec = int(month[-2:])
    year = int(month[:4])
    if mdec == 12:
        mdec = '01'
        year = year+1
    elif mdec >= 9:
        mdec = (str(mdec+1))
    else:
        mdec = '0' + str(mdec+1)

    res = str(year) + '_' + mdec
    return res


if __name__ == "__main__":
    file = r'list.txt'

    sepeate_by_size('list.txt')