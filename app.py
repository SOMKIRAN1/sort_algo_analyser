from flask import Flask, render_template, request, jsonify
import random
import json

app = Flask(__name__)

# Algorithm information
algorithms_info = {
    "bubble_sort": {
        "name": "Bubble Sort",
        "best_case": "O(n) - When array is already sorted",
        "worst_case": "O(n²) - When array is reverse sorted",
        "description": "Repeatedly compares adjacent elements and swaps them if they are in wrong order."
    },
    "selection_sort": {
        "name": "Selection Sort",
        "best_case": "O(n²)",
        "worst_case": "O(n²)",
        "description": "Finds minimum element and places it at the beginning repeatedly."
    },
    "insertion_sort": {
        "name": "Insertion Sort",
        "best_case": "O(n) - When array is already sorted",
        "worst_case": "O(n²) - When array is reverse sorted",
        "description": "Builds sorted array one item at a time by inserting elements in correct position."
    },
    "merge_sort": {
        "name": "Merge Sort",
        "best_case": "O(n log n)",
        "worst_case": "O(n log n)",
        "description": "Divides array into halves, sorts them, and merges the sorted halves."
    },
    "quick_sort": {
        "name": "Quick Sort",
        "best_case": "O(n log n)",
        "worst_case": "O(n²) - When pivot is always smallest/largest",
        "description": "Picks pivot element and partitions array around the pivot."
    }
}

class SortingVisualizer:
    def __init__(self):
        self.steps = []
        self.explanations = []
        self.logic_explanations = []
        self.highlights = []
    
    def bubble_sort(self, arr):
        self.steps = [arr.copy()]
        self.explanations = ["Starting Bubble Sort Algorithm"]
        self.logic_explanations = ["Bubble sort works by repeatedly comparing adjacent elements and swapping them if they are in the wrong order. Each pass through the list places the next largest value in its proper place."]
        self.highlights = [{"comparing": [], "swapping": [], "sorted": [], "pivot": []}]
        
        n = len(arr)
        for i in range(n):
            swapped = False
            self.steps.append(arr.copy())
            self.explanations.append(f"🔄 Starting Pass {i+1}")
            self.logic_explanations.append(f"Pass {i+1}: Compare adjacent elements. Largest element will bubble to position {n-i-1}.")
            self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(n-i, n)), "pivot": []})
            
            for j in range(0, n-i-1):
                # Comparing step
                self.steps.append(arr.copy())
                self.explanations.append(f"🔍 Comparing: {arr[j]} and {arr[j+1]}")
                self.logic_explanations.append(f"Check if {arr[j]} > {arr[j+1]}. If yes, swap to maintain order.")
                self.highlights.append({"comparing": [j, j+1], "swapping": [], "sorted": list(range(n-i, n)), "pivot": []})
                
                if arr[j] > arr[j+1]:
                    # Swap step
                    arr[j], arr[j+1] = arr[j+1], arr[j]
                    swapped = True
                    self.steps.append(arr.copy())
                    self.explanations.append(f"🔄 Swapped {arr[j]} and {arr[j+1]}")
                    self.logic_explanations.append(f"Swapped because {arr[j+1]} was greater than {arr[j]}.")
                    self.highlights.append({"comparing": [], "swapping": [j, j+1], "sorted": list(range(n-i, n)), "pivot": []})
            
            if not swapped:
                break
        
        self.steps.append(arr.copy())
        self.explanations.append("🎉 Sorting Completed!")
        self.logic_explanations.append("Array is now sorted in ascending order.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(n)), "pivot": []})
        return self.steps, self.explanations, self.logic_explanations, self.highlights

    def selection_sort(self, arr):
        self.steps = [arr.copy()]
        self.explanations = ["Starting Selection Sort Algorithm"]
        self.logic_explanations = ["Selection sort divides the array into sorted and unsorted parts. It repeatedly finds the minimum element from unsorted part and puts it at the beginning."]
        self.highlights = [{"comparing": [], "swapping": [], "sorted": [], "pivot": []}]
        
        n = len(arr)
        for i in range(n):
            min_idx = i
            self.steps.append(arr.copy())
            self.explanations.append(f"🔍 Finding min in positions {i} to {n-1}")
            self.logic_explanations.append(f"Find smallest element in unsorted portion starting from index {i}.")
            self.highlights.append({"comparing": [i], "swapping": [], "sorted": list(range(i)), "pivot": []})
            
            for j in range(i+1, n):
                self.steps.append(arr.copy())
                self.explanations.append(f"📊 Comparing: {arr[j]} vs current min {arr[min_idx]}")
                self.logic_explanations.append(f"Check if {arr[j]} < {arr[min_idx]} to find new minimum.")
                self.highlights.append({"comparing": [min_idx, j], "swapping": [], "sorted": list(range(i)), "pivot": []})
                
                if arr[j] < arr[min_idx]:
                    min_idx = j
            
            if min_idx != i:
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                self.steps.append(arr.copy())
                self.explanations.append(f"🔄 Moved min {arr[i]} to position {i}")
                self.logic_explanations.append(f"Placed minimum element at its correct sorted position.")
                self.highlights.append({"comparing": [], "swapping": [i, min_idx], "sorted": list(range(i+1)), "pivot": []})
        
        self.steps.append(arr.copy())
        self.explanations.append("🎉 Sorting Completed!")
        self.logic_explanations.append("Array is now sorted in ascending order.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(n)), "pivot": []})
        return self.steps, self.explanations, self.logic_explanations, self.highlights

    def insertion_sort(self, arr):
        self.steps = [arr.copy()]
        self.explanations = ["Starting Insertion Sort Algorithm"]
        self.logic_explanations = ["Insertion sort builds the final sorted array one item at a time by inserting each element into its proper position."]
        self.highlights = [{"comparing": [], "swapping": [], "sorted": [0], "pivot": []}]
        
        n = len(arr)
        for i in range(1, n):
            key = arr[i]
            j = i-1
            
            self.steps.append(arr.copy())
            self.explanations.append(f"🔍 Inserting {key} into sorted portion")
            self.logic_explanations.append(f"Insert element {key} into already sorted part (0 to {i-1}).")
            self.highlights.append({"comparing": [i], "swapping": [], "sorted": list(range(i)), "pivot": []})
            
            while j >= 0 and key < arr[j]:
                arr[j+1] = arr[j]
                j -= 1
                self.steps.append(arr.copy())
                self.explanations.append(f"➡️ Shifting elements for {key}")
                self.logic_explanations.append(f"Shift elements right to make space for {key}.")
                self.highlights.append({"comparing": [j+1], "swapping": [], "sorted": list(range(i)), "pivot": []})
            
            arr[j+1] = key
            self.steps.append(arr.copy())
            self.explanations.append(f"✅ {key} inserted at position {j+1}")
            self.logic_explanations.append(f"Element placed in correct sorted position.")
            self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(i+1)), "pivot": []})
        
        self.steps.append(arr.copy())
        self.explanations.append("🎉 Sorting Completed!")
        self.logic_explanations.append("Array is now sorted in ascending order.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(n)), "pivot": []})
        return self.steps, self.explanations, self.logic_explanations, self.highlights

    def merge_sort(self, arr):
        self.steps = [arr.copy()]
        self.explanations = ["Starting Merge Sort Algorithm"]
        self.logic_explanations = ["Merge sort uses divide and conquer approach. It divides the array into halves, sorts them, and merges the sorted halves."]
        self.highlights = [{"comparing": [], "swapping": [], "sorted": [], "pivot": []}]
        
        def merge_sort_helper(low, high):
            if low < high:
                mid = (low + high) // 2
                
                self.steps.append(arr.copy())
                self.explanations.append(f"📊 Dividing: indices {low} to {high}")
                self.logic_explanations.append(f"Split array from index {low} to {high} at mid-point {mid}.")
                self.highlights.append({"comparing": list(range(low, high+1)), "swapping": [], "sorted": [], "pivot": []})
                
                merge_sort_helper(low, mid)
                merge_sort_helper(mid+1, high)
                
                self.merge(arr, low, mid, high)
        
        merge_sort_helper(0, len(arr)-1)
        
        self.steps.append(arr.copy())
        self.explanations.append("🎉 Sorting Completed!")
        self.logic_explanations.append("Array is now sorted using merge sort.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(len(arr))), "pivot": []})
        return self.steps, self.explanations, self.logic_explanations, self.highlights

    def merge(self, arr, low, mid, high):
        left = arr[low:mid+1]
        right = arr[mid+1:high+1]
        
        i = j = 0
        k = low
        
        while i < len(left) and j < len(right):
            self.steps.append(arr.copy())
            self.explanations.append(f"🔀 Merging: comparing {left[i]} and {right[j]}")
            self.logic_explanations.append(f"Compare elements from left and right halves during merge.")
            self.highlights.append({"comparing": [k], "swapping": [], "sorted": [], "pivot": []})
            
            if left[i] <= right[j]:
                arr[k] = left[i]
                i += 1
            else:
                arr[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    def quick_sort(self, arr):
        self.steps = [arr.copy()]
        self.explanations = ["Starting Quick Sort Algorithm"]
        self.logic_explanations = ["Quick sort picks a pivot element and partitions the array around the pivot. Elements smaller than pivot go left, larger go right."]
        self.highlights = [{"comparing": [], "swapping": [], "sorted": [], "pivot": []}]
        
        def quick_sort_helper(low, high):
            if low < high:
                pi = self.partition(arr, low, high)
                
                self.steps.append(arr.copy())
                self.explanations.append(f"🎯 Partitioned around pivot at index {pi}")
                self.logic_explanations.append(f"Pivot {arr[pi]} is now in correct position. Recursively sort left and right partitions.")
                self.highlights.append({"comparing": [], "swapping": [], "sorted": [pi], "pivot": [pi]})
                
                quick_sort_helper(low, pi-1)
                quick_sort_helper(pi+1, high)
        
        quick_sort_helper(0, len(arr)-1)
        
        self.steps.append(arr.copy())
        self.explanations.append("🎉 Sorting Completed!")
        self.logic_explanations.append("Array is now sorted using quick sort.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": list(range(len(arr))), "pivot": []})
        return self.steps, self.explanations, self.logic_explanations, self.highlights

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low - 1
        
        self.steps.append(arr.copy())
        self.explanations.append(f"📌 Choosing pivot: {pivot} at index {high}")
        self.logic_explanations.append(f"Partition array around pivot {pivot}. Elements < pivot go left, > pivot go right.")
        self.highlights.append({"comparing": [], "swapping": [], "sorted": [], "pivot": [high]})
        
        for j in range(low, high):
            self.steps.append(arr.copy())
            self.explanations.append(f"🔍 Comparing {arr[j]} with pivot {pivot}")
            self.logic_explanations.append(f"Check if {arr[j]} <= pivot to decide placement.")
            self.highlights.append({"comparing": [j, high], "swapping": [], "sorted": [], "pivot": [high]})
            
            if arr[j] <= pivot:
                i += 1
                if i != j:
                    arr[i], arr[j] = arr[j], arr[i]
                    self.steps.append(arr.copy())
                    self.explanations.append(f"🔄 Swapped {arr[i]} and {arr[j]}")
                    self.logic_explanations.append(f"Swapped to maintain partition order.")
                    self.highlights.append({"comparing": [], "swapping": [i, j], "sorted": [], "pivot": [high]})
        
        arr[i+1], arr[high] = arr[high], arr[i+1]
        return i+1

visualizer = SortingVisualizer()

def generate_array(size, array_type='random'):
    # Perfect balance: numbers are small and have good visual difference
    # Values between 1-30 with good spacing
    
    if array_type == 'sorted':
        # Create evenly spaced values: 5, 10, 15, 20, ...
        return [5 + i * 3 for i in range(size)]
    elif array_type == 'reverse_sorted':
        # Reverse of above
        return [5 + (size - 1 - i) * 3 for i in range(size)]
    else:
        # Random but with good visual distinction
        return [random.randint(5, 30) for _ in range(size)]

@app.route('/')
def index():
    return render_template('index.html', algorithms=algorithms_info)

@app.route('/generate_array', methods=['POST'])
def generate_array_route():
    data = request.get_json()
    size = data.get('size', 10)
    array_type = data.get('type', 'random')
    array = generate_array(size, array_type)
    return jsonify({'array': array})

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    algorithm = data.get('algorithm')
    array = data.get('array')
    
    arr = [int(x) for x in array]
    
    if algorithm == 'bubble_sort':
        steps, explanations, logic_explanations, highlights = visualizer.bubble_sort(arr.copy())
    elif algorithm == 'selection_sort':
        steps, explanations, logic_explanations, highlights = visualizer.selection_sort(arr.copy())
    elif algorithm == 'insertion_sort':
        steps, explanations, logic_explanations, highlights = visualizer.insertion_sort(arr.copy())
    elif algorithm == 'merge_sort':
        steps, explanations, logic_explanations, highlights = visualizer.merge_sort(arr.copy())
    elif algorithm == 'quick_sort':
        steps, explanations, logic_explanations, highlights = visualizer.quick_sort(arr.copy())
    else:
        return jsonify({'error': 'Algorithm not found'})
    
    return jsonify({
        'steps': steps,
        'explanations': explanations,
        'logic_explanations': logic_explanations,
        'highlights': highlights,
        'total_steps': len(steps)
    })

if __name__ == '__main__':
    app.run(debug=True)