# Example 1: Generate a Function

## Prompt in Continue Chat:

```
Create a JavaScript function that:
1. Takes an array of numbers
2. Filters out negative numbers
3. Squares each remaining number
4. Returns the sum

Include JSDoc comments and error handling.
```

## Expected Output:

```javascript
/**
 * Processes an array of numbers by filtering negatives, squaring, and summing
 * @param {number[]} numbers - Array of numbers to process
 * @returns {number} Sum of squared positive numbers
 * @throws {TypeError} If input is not an array or contains non-numbers
 */
function processNumbers(numbers) {
  if (!Array.isArray(numbers)) {
    throw new TypeError('Input must be an array');
  }
  
  if (numbers.some(n => typeof n !== 'number' || isNaN(n))) {
    throw new TypeError('Array must contain only valid numbers');
  }
  
  return numbers
    .filter(n => n >= 0)
    .map(n => n * n)
    .reduce((sum, n) => sum + n, 0);
}

// Example usage:
console.log(processNumbers([1, -2, 3, 4, -5])); // Output: 26 (1 + 9 + 16)
```

## How to Use:
1. Open Continue panel (Cmd/Ctrl + L)
2. Paste the prompt
3. Click "Insert at cursor" to add to your file
