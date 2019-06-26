import os
import time
import datetime





def get_dir(rootdir):
    list = os.listdir(rootdir)
    dirname = []
    dirfile = []
    for name in list:
        pathname = os.path.join(rootdir, name)
        if os.path.isdir(pathname):
            dirname.append(pathname)
            with open('/tmp/path_plog.txt', 'a') as pa:
                pa.write(pathname+'\n')
            get_dir(pathname)
        else:
            dirfile.append(pathname)


def t_date(files):
    # get current time
    today = datetime.datetime.now()
    # set
    offset = datetime.timedelta(days=-3)
    get_date = (today+offset)
    final_time = time.mktime(get_date.timetuple())
    filetime = os.path.getatime(files)
    timeArray = time.localtime(filetime)
    otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
    if filetime >= final_time:
        return files, otherStyleTime

def get_files(file_path):
    list = []
    tmp = []
    with open(file_path, 'r') as f:
        for line in f.readlines():
            list.append(line.strip('\n'))
        for pathname in list:
            for y in os.listdir(pathname):
                if os.path.isfile(os.path.join(pathname, y)):
                    files = t_date(os.path.join(pathname, y))
                    if files == None:
                        continue
                    else:
                        filename = files[0]
                        filetime = files[1]
                        with open('/tmp/plog_filename.txt', 'a') as w:
                            w.write(filename+':'+filetime+'\n')
                else:
                    continue

def filecmp():
    plog_tmp = os.popen('''cat /tmp/path_plog.txt | cut -d '/' -f 3-5 ''').readlines()
    yunlog_tmp = os.popen('''cat /tmp/yunniao_logs_path.txt |  cut -d '/' -f 3-5  ''').readlines()
    os.popen('''sed -i '/.*\.gz.*/d' /tmp/yunniao_logs_filename.txt  ''')
    os.popen('''sed -i '/.*\.gz.*/d' /tmp/plog_filename.txt  ''')
    plog_file_tmp = os.popen(''' cat /tmp/plog_filename.txt | cut -d '/' -f 3-10 | cut -d ':' -f 1  | sort''').readlines()
    yn_file_tmp = os.popen(''' cat /tmp/yunniao_logs_filename.txt | cut -d '/' -f 3-10 | cut -d ':' -f 1  | sort''').readlines()


    plog_to_ynlog_path = set(plog_tmp).difference(set(yunlog_tmp))
    ynlog_to_plog_path = set(yunlog_tmp).difference(set(plog_tmp))
    for x in plog_to_ynlog_path:
        with open('/tmp/plog_to_ynlog_path.txt', 'a') as py:
            py.write(x+'\n')
    for y in ynlog_to_plog_path:
        with open('/tmp/ynlog_to_plog_path.txt', 'a') as yp:
            yp.write(y+'\n')

    plog_to_ynlog_file=set(plog_file_tmp).difference(set(yn_file_tmp))
    ynlog_to_plog_file=set(yn_file_tmp).difference(set(plog_file_tmp))
    
    for z in plog_to_ynlog_file:
        with open('/tmp/plog_to_ynlog_file.txt','a') as pf:
            pf.write(z+'\n')
    for i in ynlog_to_plog_file:
        with open('/tmp/ynlog_to_plog_file.txt','a') as yf:
            yf.write(i+'\n')

def man():
    Flag=False
    Dirname=[]
    while not Flag:
        i = 0
        Dirname[i] = input('dirname:')
        if Dirname[i] == Q:
            Flag = True
            break
        else:
            i+=1 
    
    
    for dirname in Dirname:
        file_dir = '/tmp{0}.txt'.format(dirname)
        print(file_dir)
        get_dir(dirname)
        get_files(file_dir)
#    filecmp()


if __name__ == "__main__":

    man()
