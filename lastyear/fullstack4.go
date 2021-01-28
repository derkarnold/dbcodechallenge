package main

import (
	"fmt"
)

// Implement the doSwap() method for the ByteSwapper which:
// reads an array of four bytes from input channel swapper.in
// makes a new array with the bytes swapped like this {a, b, c, d} -> {c, d, b, a}
// and pushes it to the output channel swapper.out

const arrLength = 4

func (swapper *ByteSwapper) doSwap() {
	inputArray := <-swapper.in
	outputArray := [arrLength]byte{
		inputArray[2], inputArray[3],
		inputArray[1], inputArray[0],
	}
	swapper.out <- outputArray
}

type ByteSwapper struct {
	in  chan [arrLength]byte
	out chan [arrLength]byte
}

func StartNewSwapper() ByteSwapper {
	swapper := ByteSwapper{
		in:  make(chan [arrLength]byte),
		out: make(chan [arrLength]byte)}
	go swapper.doSwap()
	return swapper
}

func doTheMagic() []byte {
	arr := [...]byte{0x27, 0x62, 0xa7, 0xbd, 0x19, 0xf2, 0x46,
		0x9c, 0x8b, 0x77, 0x5b, 0x35, 0x45, 0x17, 0xa8, 0xb6}

	swappers := make(map[int]ByteSwapper)
	for i := 0; i < len(arr); i += arrLength {
		swappers[i] = StartNewSwapper()
	}
	for i := 0; i < len(arr); i += arrLength {
		slice := arr[i : i+arrLength]
		arg := [arrLength]byte{}
		copy(arg[:], slice)

		arg[0] = arg[0] ^ arg[3]
		arg[2] = arg[1] ^ arg[0]

		swappers[i].in <- arg
	}
	fmt.Print("receiving some bytes")
	return assembleBytes(swappers)
}

func assembleBytes(swappers map[int]ByteSwapper) []byte {
	slice := make([]byte, 0)
	list := [arrLength]int{0, 12, 8, 4}
	for i := 0; i < arrLength; i++ {
		bytes := <-swappers[list[i]].out
		fmt.Print(".")
		slice = append(slice, bytes[:]...)
	}
	fmt.Print("\n")
	return slice
}

func main() {
	slice := doTheMagic()
	fmt.Printf("%x-%x-%x-%x\n", slice[0:4], slice[4:6], slice[6:8], slice[8:16])
}
