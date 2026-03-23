package main

import "errors"

type arrayList[T any] struct {
	data     []T
	size     int
	capacity int
}

func NewArrayList[T any]() *arrayList[T] {
	return &arrayList[T]{
		data:     make([]T, 5),
		size:     0,
		capacity: 5,
	}
}

func (a *arrayList[T]) Add(data T) {
	if a.size == a.capacity {
		a.Grow()
	}

	a.data[a.size] = data
	a.size++
}

func (a *arrayList[T]) Get(index int) (T, error) {
	var t T
	if 0 > index || index >= a.size {
		return t, errors.New("index out of bound")
	}

	return a.data[index], nil
}

func (a *arrayList[T]) Remove(index int) error {
	if 0 > index || index >= a.size {
		return errors.New("index out of bound")
	}

	for i := index; i < a.size-1; i++ {
		a.data[i] = a.data[i+1]
	}

	var t T
	a.size--
	a.data[a.size] = t

	return nil
}

func (a *arrayList[T]) Grow() {
	a.capacity *= 2
	newData := make([]T, a.capacity)
	copy(newData, a.data)
	a.data = newData
}
