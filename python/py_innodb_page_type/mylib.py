#encoding=utf-8
import os
import sys
import codecs
from include import *

version3_flag=False
if sys.version>'3':
   version3_flag=True

                
def mach_read_from_n(page,start_offset,length):
    ret = page[start_offset:start_offset+length]
    res=None
    if version3_flag:
        res=codecs.encode(ret,encoding='hex')
    else:
        res=codecs.encode(ret,'hex')

    return res
        
def get_innodb_page_type(**kw):
    f=open(kw["tablespace"],'rb')
    fsize = os.path.getsize(f.name)/INNODB_PAGE_SIZE
    fsize=int(fsize)
    ret = {}
    with open(kw['output'],'w+') as fp:
        fp.write("Total number of page: {0}\n".format(fsize))
        fp.write("{0}\n".format('--'*30))
        for i in range(fsize):
            page = f.read(INNODB_PAGE_SIZE)
            page_offset = mach_read_from_n(page,FIL_PAGE_OFFSET,4)
            page_type = mach_read_from_n(page,FIL_PAGE_TYPE,2)
            if version3_flag:
               page_type=page_type.decode('utf-8')

            if kw["v"]:
               msg="page offset {0}, page type {1}".format(page_offset,innodb_page_type[page_type])
               if page_type == '45bf':
                  page_level = mach_read_from_n(page,FIL_PAGE_DATA+PAGE_LEVEL,2)
                  msg="{0}, page level {1}".format(msg,page_level)

               fp.write('{0}\n'.format(msg))

            if page_type not in  ret:
               ret[page_type] = 1
            else:
               ret[page_type] = ret[page_type] + 1

        fp.write("{0}\n".format('--'*30))
        for type in ret:
            fp.write("{0}: {1}\n".format(innodb_page_type[type],ret[type]))

    f.close()
