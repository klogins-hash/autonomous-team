# Example 4: Generate Tests

## Your Function:

```javascript
function validateEmail(email) {
  const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return regex.test(email);
}
```

## Prompt (Highlight function → Continue chat):

```
Write comprehensive unit tests for this function using Jest.
Include edge cases and invalid inputs.
```

## Expected Output:

```javascript
describe('validateEmail', () => {
  describe('Valid emails', () => {
    test('should accept standard email', () => {
      expect(validateEmail('user@example.com')).toBe(true);
    });

    test('should accept email with subdomain', () => {
      expect(validateEmail('user@mail.example.com')).toBe(true);
    });

    test('should accept email with plus sign', () => {
      expect(validateEmail('user+tag@example.com')).toBe(true);
    });

    test('should accept email with numbers', () => {
      expect(validateEmail('user123@example456.com')).toBe(true);
    });

    test('should accept email with dots in local part', () => {
      expect(validateEmail('first.last@example.com')).toBe(true);
    });
  });

  describe('Invalid emails', () => {
    test('should reject email without @', () => {
      expect(validateEmail('userexample.com')).toBe(false);
    });

    test('should reject email without domain', () => {
      expect(validateEmail('user@')).toBe(false);
    });

    test('should reject email without local part', () => {
      expect(validateEmail('@example.com')).toBe(false);
    });

    test('should reject email without TLD', () => {
      expect(validateEmail('user@example')).toBe(false);
    });

    test('should reject email with spaces', () => {
      expect(validateEmail('user @example.com')).toBe(false);
    });

    test('should reject empty string', () => {
      expect(validateEmail('')).toBe(false);
    });

    test('should reject multiple @ symbols', () => {
      expect(validateEmail('user@@example.com')).toBe(false);
    });
  });

  describe('Edge cases', () => {
    test('should handle null', () => {
      expect(validateEmail(null)).toBe(false);
    });

    test('should handle undefined', () => {
      expect(validateEmail(undefined)).toBe(false);
    });

    test('should handle non-string input', () => {
      expect(validateEmail(123)).toBe(false);
    });
  });
});
```

## How to Use:
1. Write your function
2. Highlight it
3. Ask Continue to write tests
4. Copy tests to your test file
5. Run: `npm test`
