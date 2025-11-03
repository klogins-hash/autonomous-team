# Example 3: Debug an Error

## Your Code with Error:

```python
def calculate_average(numbers):
    total = sum(numbers)
    return total / len(numbers)

# This crashes!
result = calculate_average([])
print(result)
```

## Error Message:
```
ZeroDivisionError: division by zero
```

## Prompt in Continue Chat:

```
I'm getting this error:
ZeroDivisionError: division by zero

Here's my code:
[paste code above]

What's wrong and how do I fix it?
```

## Claude's Response:

```
The issue is that you're dividing by len(numbers) which is 0 when the list is empty.

Here's the fixed version with proper error handling:

```python
def calculate_average(numbers):
    """
    Calculate the average of a list of numbers.
    
    Args:
        numbers: List of numbers
        
    Returns:
        float: The average, or None if list is empty
        
    Raises:
        TypeError: If numbers is not a list or contains non-numeric values
    """
    if not isinstance(numbers, list):
        raise TypeError("Input must be a list")
    
    if not numbers:  # Empty list check
        return None
    
    if not all(isinstance(n, (int, float)) for n in numbers):
        raise TypeError("All elements must be numbers")
    
    total = sum(numbers)
    return total / len(numbers)

# Safe usage:
result = calculate_average([])
if result is None:
    print("Cannot calculate average of empty list")
else:
    print(f"Average: {result}")

# With data:
result = calculate_average([1, 2, 3, 4, 5])
print(f"Average: {result}")  # Output: Average: 3.0
```

**What changed:**
1. Added empty list check before division
2. Returns None for empty lists instead of crashing
3. Added type checking
4. Added comprehensive docstring
5. Added example of safe usage
```

## How to Use:
1. Copy error message
2. Open Continue chat
3. Explain the problem and paste code + error
4. Get explanation and fixed code
