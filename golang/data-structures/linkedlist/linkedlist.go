package main

import (
	"errors"
	"fmt"
)

type llnode[T any] struct {
	value T
	next  *llnode[T]
}

type llist[T any] struct {
	head *llnode[T]
	tail *llnode[T]
	len  int
}

func NewLlist[T any]() *llist[T] {
	return &llist[T]{}
}

func (l *llist[T]) Size() int {
	return l.len
}

func (l *llist[T]) Add(value T) {
	l.len++
	newNode := &llnode[T]{value: value}

	if l.head == nil {
		l.head, l.tail = newNode, newNode
		return
	}

	l.tail.next = newNode
	l.tail = newNode
}

func (l *llist[T]) PushFront(value T) {
	newNode := &llnode[T]{
		value: value,
		next:  l.head,
	}

	l.head = newNode
	l.len++
}

func (l *llist[T]) InsertAt(index int, value T) error {
	if 0 > index || index > l.len {
		return errors.New("index out of bound")
	}

	if index == 0 {
		l.PushFront(value)
		return nil
	}

	if index == l.len {
		l.Add(value)
		return nil
	}

	toPushNode := l.head
	for range index - 1 {
		toPushNode = toPushNode.next
	}

	newNode := &llnode[T]{
		value: value,
		next:  toPushNode.next,
	}

	toPushNode.next = newNode
	l.len++

	return nil
}

func (l *llist[T]) RemoveAt(index int) error {
	if 0 > index || index >= l.len {
		return errors.New("index out of bound")
	}

	if index == 0 {
		l.head = l.head.next
		if l.head == nil {
			l.tail = nil
		}

		l.len--
		return nil
	}

	before := l.head
	for range index - 1 {
		before = before.next
	}

	before.next = before.next.next
	if before.next == nil {
		l.tail = before
	}

	l.len--
	return nil
}

func (l *llist[T]) Display() {
	curr := l.head
	for curr != nil {
		fmt.Printf("%v -> ", curr.value)
		curr = curr.next
	}

	fmt.Println("nil")
}
