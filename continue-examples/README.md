# Continue.dev Examples

Real-world examples of using Continue.dev with Claude in your code-server.

## Examples Included

1. **example1-generate-function.md** - Generate new functions from descriptions
2. **example2-refactor-code.md** - Refactor and improve existing code
3. **example3-debug-error.md** - Debug errors with AI assistance
4. **example4-write-tests.md** - Generate comprehensive unit tests

## Quick Start

1. **Get your API key**: https://console.anthropic.com/
2. **Add it to config**: Edit `/root/.continue/config.json`
3. **Open Continue**: Press `Cmd/Ctrl + L` in code-server
4. **Try an example**: Copy a prompt from any example file

## Keyboard Shortcuts

- `Cmd/Ctrl + L` - Open Continue chat
- `Cmd/Ctrl + I` - Inline edit (highlight code first)
- `Tab` - Accept autocomplete
- `Esc` - Reject autocomplete

## More Examples

### Generate a React Component
```
Create a React component for a login form with:
- Email and password fields
- Form validation
- Submit button
- Loading state
- Error handling
Use TypeScript and Tailwind CSS
```

### Create API Endpoints
```
Create Express.js REST API endpoints for a blog:
- GET /posts - list all posts
- GET /posts/:id - get single post
- POST /posts - create post (auth required)
- PUT /posts/:id - update post (auth required)
- DELETE /posts/:id - delete post (auth required)
Include middleware for authentication
```

### Write Documentation
```
@myfile.js Generate comprehensive JSDoc comments for all functions in this file
```

### Convert Code
```
Convert this JavaScript code to TypeScript with proper types
[paste code]
```

### Optimize Performance
```
@myfile.py Analyze this code for performance issues and suggest optimizations
```

## Tips

- Be specific in your prompts
- Use `@filename` to reference files
- Highlight code before using inline edit
- Review generated code before using
- Start simple, then iterate

## Read the Full Guide

See `/root/continue-guide.md` for complete documentation.
