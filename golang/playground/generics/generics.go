package main

import "fmt"

// [T int | string | bool]
// [T int, V string]
func printSlice[T any](items []T) {
	for _, item := range items {
		fmt.Print(item, " ")
	}

	fmt.Println()
}

type stack[T any] struct {
	elements []T
}

func main() {
	nums := []int{1, 2, 3}
	printSlice(nums)

	names := []string{"golang", "java", "c++"}
	printSlice(names)

	mystack := stack[int]{
		elements: []int{1, 2, 3},
	}
	printSlice(mystack.elements)

	mystack2 := stack[string]{
		elements: []string{"a", "b", "c"},
	}
	printSlice(mystack2.elements)
}
