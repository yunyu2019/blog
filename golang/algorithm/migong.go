//迷宫问题
package main

import (
	"fmt"
)

func setWay(mg_map *[8][7]int, i int, j int) bool {
	if mg_map[6][5] == 2 {
		return true
	} else {
		if mg_map[i][j] == 0 {
			mg_map[i][j] = 2
			if setWay(mg_map, i+1, j) {
				return true
			} else if setWay(mg_map, i, j+1) {
				return true
			} else if setWay(mg_map, i-1, j) {
				return true
			} else if setWay(mg_map, i, j-1) {
				return true
			} else {
				mg_map[i][j] = 3
				return false
			}
		} else {
			return false
		}
	}
}

func main() {
	var mg_map [8][7]int //使用二维数组构建迷宫地图
	/*
	* 迷宫规则二维数组的值 0-没有走过的点 1-墙 2-通路 3-曾经走过，是死路
	 */
	for i := 0; i < 8; i++ {
		for j := 0; j < 7; j++ {
			if i == 0 || i == 7 || j == 0 || j == 6 {
				mg_map[i][j] = 1
			}
		}
	}
	mg_map[3][1] = 1
	mg_map[3][2] = 1

	for i := 0; i < 8; i++ {
		for j := 0; j < 7; j++ {
			fmt.Print(mg_map[i][j], " ")
		}
		fmt.Println()
	}
	setWay(&mg_map, 1, 1)
	fmt.Println("找到的路径为")
	for i := 0; i < 8; i++ {
		for j := 0; j < 7; j++ {
			fmt.Print(mg_map[i][j], " ")
		}
		fmt.Println()
	}

}
