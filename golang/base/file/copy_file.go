/*
 * Author: yunyu2019
 * Date: 2019-12-12 17:06:19
 * Description:
 */

package main

import (
	"fmt"
	"io"
	"os"
)

func CopyFile(source string, dist string) (n int64, err error) {
	f, err := os.Open(source)
	if err != nil {
		return
	}
	defer f.Close()

	w, err := os.OpenFile(dist, os.O_WRONLY|os.O_CREATE, os.ModePerm)
	if err != nil {
		return
	}
	defer w.Close()
	return io.Copy(w, f)
}

func main() {
	source := "d:/test.flv"
	dist := "e:/test.flv"
	_, err := CopyFile(source, dist)
	fmt.Println(err)
}
