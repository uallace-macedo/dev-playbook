package main

import "fmt"

// by value
func changeNum(num int) {
	num = 5
	fmt.Println("In changeNum", num)
}

// by reference
func changeNumPointer(num *int) {
	*num = 5
	fmt.Println("In changeNumPointer", &num)
}

func main() {
	num := 1
	changeNum(num)

	fmt.Println("After changeNum in main", num)

	changeNumPointer(&num)
	fmt.Println("After changeNumPointer in main", num)
}
