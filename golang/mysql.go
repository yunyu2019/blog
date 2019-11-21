/*
 * @Description: In User Settings Edit
 * @Author: your name
 * @Date: 2019-04-11 11:01:08
 * @LastEditTime: 2019-08-27 14:21:53
 * @LastEditors: Please set LastEditors
 */
package main

import (
	"database/sql"
	"fmt"

	_ "github.com/go-sql-driver/mysql"
)

func main() {
	db, err := sql.Open("mysql", "root:123456@/test")
	if err != nil {
		panic(err.Error())
	}
	defer db.Close()
	stmtOut, err := db.Prepare("SELECT id,name,daoyan,bianju FROM douban WHERE daoyan = ? limit ?,?")
	if err != nil {
		panic(err.Error())
	}
	defer stmtOut.Close()
	var (
		daoyan    string
		page      int
		page_size int
		id        int
		name      string
		bianju    string
	)
	daoyan = "宫崎骏"
	page = 0
	page_size = 10

	rows, err := stmtOut.Query(daoyan, page, page_size)
	if err != nil {
		panic(err.Error())
	}
	defer rows.Close()
	for rows.Next() {
		err := rows.Scan(&id, &name, &daoyan, &bianju)
		if err != nil {
			fmt.Println(err.Error())
			break
		}
		fmt.Println(id, name, daoyan, bianju)
	}
}
