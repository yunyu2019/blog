package main

import (
	"database/sql"
	"flag"
	"fmt"
	"os"
	"strings"

	_ "github.com/go-sql-driver/mysql"
)

// Field 表字段结构
type Field struct {
	fieldName     string
	fieldDesc     string
	dataType      string
	isNull        string
	length        int
	columnType    string
	columnDefault string
}

var conn *sql.DB

// getDictPath 获取输出目录路径
func getDictPath(distPath string) (s string, err error) {
	if distPath == "" {
		dir, err := os.Getwd()
		if err != nil {
			return "", err
		}
		distPath = dir + string(os.PathSeparator) + "mysql_dict"
	}
	if _, err := os.Stat(distPath); os.IsNotExist(err) {
		fmt.Println(distPath)
		os.MkdirAll(distPath, 0755)
	}
	return distPath, nil
}

//过滤表注解信息
func trimComment(comment, table string) string {
	comment = strings.Replace(comment, table, "", -1)
	comment = strings.Replace(comment, "(", "", -1)
	comment = strings.Replace(comment, ")", "", -1)
	comment = strings.Replace(comment, "\n", "", -1)
	return comment
}

func trimColumn(comment string) string {
	comment = strings.Trim(comment, " ")
	comment = strings.Replace(comment, "\r\n", "", -1)
	return comment
}

// initMysql 初始化数据库链接
func initMysql(dsn string) (err error) {
	conn, err = sql.Open("mysql", dsn)
	if err != nil {
		fmt.Printf("open mysql error,error:%v\n", err)
		return err
	}

	if err = conn.Ping(); err != nil {
		fmt.Printf("mysql connect error,error:%v\n", err)
		return err
	}

	return nil
}

// getTables获取要导出的表信息
func getTables(table string) (dbTables []string, err error) {
	dbTables = make([]string, 0)
	if table == "" {
		tableSQL := "show tables"
		row, err := conn.Query(tableSQL)
		if err != nil {
			fmt.Printf("获取db:%s 表结构失败\n", err)
			return dbTables, err
		}

		var variable string
		for row.Next() {
			err = row.Scan(&variable)
			if err != nil {
				fmt.Println("查询发生错误")
				continue
			}
			dbTables = append(dbTables, variable)
		}
		row.Close()
	} else {
		dbTables = strings.Split(table, ",")
	}
	return dbTables, nil
}

func getTableFields(dbName, tableName string) ([]Field, error) {
	sqlStr := `SELECT COLUMN_NAME fName,column_comment fDesc,DATA_TYPE dataType,IS_NULLABLE isNull,IFNULL(CHARACTER_MAXIMUM_LENGTH,0) sLength,column_type fType,IFNULL(column_default,'') fDefault FROM information_schema.columns WHERE table_schema = ? AND table_name = ?`

	var result []Field

	rows, err := conn.Query(sqlStr, dbName, tableName)
	if err != nil {
		return result, err
	}

	for rows.Next() {
		var f Field
		err = rows.Scan(&f.fieldName, &f.fieldDesc, &f.dataType, &f.isNull, &f.length, &f.columnType, &f.columnDefault)
		if err != nil {
			continue
		}

		result = append(result, f)
	}
	return result, nil
}

func run(distPath, db string, dbTables []string) {
	fileName := distPath + string(os.PathSeparator) + db + ".md"
	fp, err := os.OpenFile(fileName, os.O_CREATE|os.O_TRUNC|os.O_RDWR, 0755)
	if err != nil {
		fmt.Printf("打开文件%s 失败,error:%v\n", fileName, err)
		return
	}
	fmt.Printf("表结构即将导入路径:%s\n", fileName)
	i := 0

	var content string
	for _, table := range dbTables {
		var tableComment string
		fmt.Printf("查询表%s的状态\n", table)
		tableSQL := "select table_comment from information_schema.`tables` where UPPER(table_type)='BASE TABLE' and LOWER(table_schema) = ? and table_name = ?"
		row := conn.QueryRow(tableSQL, db, table)
		err := row.Scan(&tableComment)
		if err != nil {
			fmt.Printf("查询表%s.%s 状态失败,error:%v\n", db, table, err)
			continue
		}

		fields, err := getTableFields(db, table)
		if err != nil {
			fmt.Printf("查询表%s.%s 结构失败,error:%v\n", db, table, err)
			continue
		}

		if len(fields) < 1 {
			fmt.Printf("查询表%s.%s 结构失败\n", db, table)
			continue
		}

		if tableComment != "" {
			tableComment = trimComment(tableComment, table)
		}

		fmt.Printf("开始生成表%s的数据结构\n", table)

		content = "#### " + table + " (" + tableComment + ")\n"
		content += "| 字段名称 | 字段类型 | IS_NULL | 默认值 | 字段注释 |\n"
		content += "| --- | --- | --- | --- | --- |\n"

		for _, v := range fields {
			if v.fieldDesc != "" {
				v.fieldDesc = trimColumn(v.fieldDesc)
			}
			content += "| " + v.fieldName + " | " + v.columnType + " | " + v.isNull + " | " + v.columnDefault + " | " + v.fieldDesc + " |\n"
		}

		fp.WriteString(content + "\n")
		fmt.Printf("表%s的数据结构生成完成\n", table)
		i++
	}
	fp.Close()
	fmt.Printf("此次共计导入%d张表结构\n", i)
}

func main() {
	var host, user, pwd, db, table, distPath string
	var port int
	flag.StringVar(&host, "host", "127.0.0.1", "mysql connect host")
	flag.IntVar(&port, "port", 3306, "mysql connect port")
	flag.StringVar(&user, "user", "root", "mysql connect user")

	flag.StringVar(&pwd, "pwd", "", "mysql connect password")
	flag.StringVar(&db, "db", "", "mysql connect db")
	flag.StringVar(&table, "table", "", "choose mysql tables")

	flag.StringVar(&distPath, "dist", "", "export mysql database file path")
	flag.Parse()

	if db == "" {
		fmt.Println("需要输入db参数")
		return
	}

	var err error
	distPath, err = getDictPath(distPath)
	if err != nil {
		fmt.Printf("设置输出路径失败,err:%v\n", err)
		return
	}

	dsn := fmt.Sprintf("%s:%s@tcp(%s:%d)/%s?charset=utf8mb4", user, pwd, host, port, db)
	fmt.Println("当前要链接的mysql信息为:", dsn)

	err = initMysql(dsn)
	if err != nil {
		fmt.Printf("mysql 链接初始化失败,err:%v\n", err)
		return
	}

	fmt.Println("mysql connect success")
	defer conn.Close()

	dbTables, err := getTables(table)
	if err != nil {
		fmt.Printf("获取表结构失败,err:%v\n", err)
		return
	}

	if len(dbTables) < 1 {
		fmt.Printf("要导出的表结构未空,请检查表是否存在")
		return
	}
	run(distPath, db, dbTables)
}
