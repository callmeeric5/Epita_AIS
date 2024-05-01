# PALISSON Antoine

## Bubble Sort
def bubble_sort(arr):
    for i in range(len(arr)):
        flag = True

        for j in range(0, len(arr)-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
                flag = False

        if flag: break

    return arr

## Selection Sort
def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i

        for j in range(i+1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]

    return arr

## Insertion
def insertion_sort(arr):
    for i in range(1, len(arr)):
        target = arr[i]
        j = i - 1

        while j >= 0 and target < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1

        arr[j + 1] = target

    return arr

## Merge Sort
def merge(left, right):
    arr = []
    i,j = 0,0

    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            arr.append(left[i])
            i += 1
        else:
            arr.append(right[j])
            j += 1

    arr.extend(left[i:])
    arr.extend(right[j:])

    return arr

def merge_sort(arr):
    if len(arr) == 1:
        return arr
    
    mid_point = len(arr) // 2
    left = merge_sort(arr[:mid_point])
    right = merge_sort(arr[mid_point:])

    return merge(left, right)

## QuickSort
def partition(arr, low, high):
    """
    This function sets the elements greater than the pivot on the right 
    and the ones lesser than the pivot on the left.

    Variables:
        > high is the pivot position 
        > pivot is the pivot value
        > high_pos is the location of the highest element (see course)
    """
    pivot = arr[high]
    high_pos = low

    for pointer in range(low, high):
        if arr[pointer] <= pivot:
            arr[high_pos], arr[pointer] = arr[pointer], arr[high_pos]
            high_pos += 1

    arr[high_pos], arr[high] = arr[high], arr[high_pos]

    return arr, high_pos

def quick_sort(arr, low, high):
    if low < high:
        arr, pivot = partition(arr, low, high)
        quick_sort(arr, low, pivot - 1)         # recursion on the left subarray
        quick_sort(arr, pivot + 1, high)        # recursion on the right subarray

    return arr

if __name__ == '__main__':
    arr = [4,-6,2,0,8,6,9,-5,-7,5,-1,2,3,0]
    print(f"bubble sort    : {bubble_sort(arr.copy())}")
    print(f"selection sort : {selection_sort(arr.copy())}")
    print(f"insertion sort : {insertion_sort(arr.copy())}")
    print(f"merge sort     : {merge_sort(arr.copy())}")
    print(f"quick sort     : {quick_sort(arr.copy(), low = 0, high = len(arr) - 1)}")
