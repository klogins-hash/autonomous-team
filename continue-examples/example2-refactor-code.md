# Example 2: Refactor Code

## Original Code (Bad):

```javascript
function getData(id) {
  var result;
  fetch('https://api.example.com/users/' + id)
    .then(function(response) {
      return response.json();
    })
    .then(function(data) {
      result = data;
      console.log(result);
    })
    .catch(function(error) {
      console.log(error);
    });
  return result;
}
```

## Prompt (Highlight code → Cmd/Ctrl + I):

```
Refactor this to:
1. Use async/await
2. Use modern ES6+ syntax
3. Add proper error handling
4. Return the data correctly
5. Add TypeScript types
```

## Expected Output:

```typescript
async function getData(id: string): Promise<User | null> {
  try {
    const response = await fetch(`https://api.example.com/users/${id}`);
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data: User = await response.json();
    return data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    return null;
  }
}

interface User {
  id: string;
  name: string;
  email: string;
}
```

## How to Use:
1. Highlight the bad code
2. Press Cmd/Ctrl + I (inline edit)
3. Type your refactoring instructions
4. Accept or reject the changes
