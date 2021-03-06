/*
 * Author: yunyu2019
 * Date: 2019-11-21 17:29:51
 * Description:
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
