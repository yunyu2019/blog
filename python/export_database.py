#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pymysql
import os
import time
import argparse

class DataDict(object):
    def __init__(self,**kw):
        # 数据库连接配置
        self.host = kw.get('host','127.0.0.1')
        self.user = kw.get('user','root')
        self.pwd = kw.get('pwd','')
        self.port = kw.get('port',3306)
        self.db = kw.get('db','')
        self.table = kw.get('table',None)
        self.folder = kw.get('folder','mysql_dict')

    def run(self):
        """脚本执行入口"""
        try:
            conn = pymysql.connect(host=self.host, user=self.user,password=self.pwd,port=self.port,db=self.db)
            cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
        except Exception as e:
            print('数据库连接失败，请检查连接信息！'+str(e))
            exit(1)
        if not self.table:
            sql = "show tables"
            cursor.execute(sql)
            results = cursor.fetchall()
            key = 'Tables_in_' + self.db
            self.table = [row[key] for row in results]

        if not os.path.exists(self.folder):
            print('创建目录:'+self.folder)
            os.mkdir(self.folder)

        file_name = self.folder + os.sep + self.db +'.md'
        if os.path.isfile(file_name):
            print('清除文件:'+file_name)
            os.unlink(file_name)

        with open(file_name,'a',encoding="utf-8") as fp:
            for table_name in self.table:
                # 判断表是否存在
                sql = "SHOW TABLES LIKE '%s'" % (table_name,)
                cursor.execute(sql)
                result_count = cursor.rowcount
                if result_count == 0:
                    print('%s数据库中%s表名不存在，无法生成……' % (self.db_name, table_name))
                    continue
                # 表注释获取
                print('开始生成表%s的数据字典' % (table_name,))
                sql = "show table status WHERE Name = '%s'" % (table_name,)
                cursor.execute(sql)
                result = cursor.fetchone()
                table_comment = result['Comment']
                
                fp.write('#### %s (%s)' % (table_name, table_comment))
                fp.write('\n | 字段名称 | 字段类型 | 默认值 | 字段注释 |')
                fp.write('\n | --- | --- | --- | --- |')
                # 表结构查询
                field_str = "COLUMN_NAME,COLUMN_TYPE,COLUMN_DEFAULT,COLUMN_COMMENT"
                sql = "select %s from information_schema.COLUMNS where table_schema='%s' and table_name='%s'" % (field_str, self.db, table_name)
                cursor.execute(sql)
                fields = cursor.fetchall()
                for field in fields:
                    column_name = field['COLUMN_NAME']
                    column_type = field['COLUMN_TYPE']
                    column_default = str(field['COLUMN_DEFAULT'])
                    column_comment = field['COLUMN_COMMENT']
                    info = ' | ' + column_name + ' | ' + column_type + ' | ' + column_default + ' | ' + column_comment + ' | '
                    fp.write('\n ' + info)

                fp.write('\n\n')
                print('完成表%s的数据字典' % (table_name,))
        cursor.close()
        conn.close()

    def test_conn(self):
        """测试数据库连接"""
        try:
            pymysql.connect(host=self.host,user=self.user,password=self.pwd,port=self.port,db=self.db)
            return True
        except Exception as e:
            return False

# 程序执行入口
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='export mysql database struct to markdown file',prog='dbstruct')
    parser.add_argument('-a','--host',required=True,type=str,help='mysql host')
    parser.add_argument('-u','--user',required=False,default='root',type=str,help='mysql login user')
    parser.add_argument('-p','--port',required=False,default=3306,type=int,help='mysql login port')
    parser.add_argument('-pwd','--pwd',required=True,type=str,help='mysql login password')
    parser.add_argument('-db','--db',required=True,type=str,help='mysql database')
    parser.add_argument('-t','--table',nargs='*',help='choose table')
    parser.add_argument('-d','--dist',default="mysql_dict",help='export dist folder')
    args = parser.parse_args()
    host = args.host
    user = args.user
    port = args.port
    pwd = args.pwd
    db = args.db
    table = args.table
    folder = args.dist
    config = {"host":host,"user":user,"pwd":pwd,"port":port,"db":db,"table":table,"folder":folder}
    print(config)
    item = DataDict(**config)
    flag = item.test_conn()
    if not flag:
        print('mysql connect error')
        exit()

    item.run()