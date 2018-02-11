package main

import (
	"math/rand"
	"os/exec"
	"time"
	"os"
	"sync"
	"math"
)
func random(min int, max int) int {
	return rand.Intn(max-min) + min
}

func generateRandomArray(length int) []int {
	array := make([]int, length, length)
	for i:=0; i < length; i++ {
		array[i] = random(-1000, 1000)
	}
	return array
}
func algorithm(array []int) (int,int,int) {
	return findMaximumSubarray(array, 0, len(array)-1)
}
func findMaximumSubarray(array []int, low int, high int) (int, int, int) {
	if high == low {
		return low,high,array[low]
	} else {
		mid := (low+high)/2
		leftLow,leftHigh,leftSum := findMaximumSubarray(array, low, mid)
		rightLow,rightHigh,rightSum := findMaximumSubarray(array, mid + 1, high)
		crossLow,crossHigh,crossSum := findMaxCrossingSubarray(array, low, mid, high)
		if leftSum >= rightSum && leftSum >= crossSum {
			return leftLow, leftHigh, leftSum
		} else if rightSum >= leftSum && rightSum >= crossSum {
			return rightLow, rightHigh, rightSum
		} else {
			return crossLow, crossHigh, crossSum
		}
	}

}
func findMaxCrossingSubarray(array []int, low int, mid int, high int) (int, int, int) {
	leftSum := math.MinInt32
	sum := 0
	maxLeft := 0
	for i:=mid; i > low; i-- {
		sum += array[i]
		if sum > leftSum {
			leftSum = sum
			maxLeft = i
		}
	}
	rightSum := math.MinInt32
	sum = 0
	maxRight := 0
	for i:=mid+1; i < high; i++ {
		sum += array[i]
		if sum > rightSum {
			rightSum = sum
			maxRight = i
		}
	}
	return maxLeft, maxRight, leftSum+rightSum
}
func timing(array []int, result chan int, wg *sync.WaitGroup) {
	start := time.Now()
	algorithm(array)
	result <- int(time.Since(start).Nanoseconds())
	wg.Done()
}
func makeTest(length int) float64 {
	array := generateRandomArray(length)
	resultChannel := make(chan int, 4)
	wg := sync.WaitGroup{}
	for i:=0; i < 4; i++ {
		wg.Add(1)
		go timing(array, resultChannel, &wg)
	}
	wg.Wait()
	close(resultChannel)
	min := math.MaxInt32
	for resultTiming := range resultChannel {
		if resultTiming < min {
			min = resultTiming
		}
	}
	return float64(min)
}
func main() {

	testArray := []int{13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7}
	bestStartIndex, bestEndIndex, bestSum := algorithm(testArray)
	if bestStartIndex != 7 {
		panic("fail!")
	}
	if bestEndIndex != 10 {
		panic("fail!")
	}
	if bestSum != 43 {
		panic("fail!")
	}

	randomArray := generateRandomArray(1000000000)
	algorithm(randomArray)

}
func clearScreen() {
	cmd := exec.Command("clear")
	cmd.Stdout = os.Stdout
	cmd.Run()
}
