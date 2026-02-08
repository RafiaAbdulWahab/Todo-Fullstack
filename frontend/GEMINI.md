# Frontend Coding Patterns

This document outlines the coding patterns and conventions for the frontend application.

## 1. Project Structure
- Adhere to the Next.js `app` router structure.
- Organize components logically within the `src/app` directory.
- Use `components` folder for reusable UI components.
- Use `lib` for utility functions and non-UI logic.
- Use `hooks` for custom React hooks.

## 2. Next.js Specifics (Next.js 15+)
- **Server Components First**: Use Server Components by default for better performance and simpler data fetching.
- **Client Components Only When Needed**: Only use Client Components when interactivity, browser APIs, or React Hooks are required. Mark them with `'use client'`.
- **Centralized API Client**: Route all API calls through a centralized client for consistent error handling, authentication, and request/response transformation.

## 3. Naming Conventions
- Files and folders should use `kebab-case`.
- React components should use `PascalCase`.
- CSS classes should use `kebab-case`.

## 4. TypeScript
- Use TypeScript for all new code.
- Define types and interfaces clearly.
- Leverage TypeScript's strict mode where appropriate.

## 5. Styling
- Use Tailwind CSS for styling.
- Prefer utility classes for common styles.
- Create custom CSS only when necessary for complex designs or animations.
- Organize custom CSS in separate files, imported globally or within components.

## 6. State Management
- Prefer React's built-in state management (useState, useContext) for local and global state.
- Consider a dedicated state management library (e.g., Zustand, Jotai) for more complex global state needs if necessary.

## 7. API Calls
- Centralize API call logic in a dedicated service file or hook.
- Use `fetch` or a library like `axios` for HTTP requests.
- Implement error handling and loading states for all API interactions.

## 8. Performance Optimization
- Use `React.memo` and `useCallback`/`useMemo` for performance optimization where appropriate.
- Lazy load components using `next/dynamic` for improved initial load times.
- Optimize images using `next/image`.

## 9. Accessibility
- Ensure all UI components are accessible.
- Use semantic HTML.
- Provide `alt` attributes for images.
- Implement proper keyboard navigation and focus management.

## 10. Testing
- Write unit tests for components and utility functions.
- Write integration tests for key user flows.
- Use testing libraries like React Testing Library and Jest.

## 11. Linting and Formatting
- Adhere to ESLint rules as configured in the project.
- Use Prettier for code formatting.

## 12. Comments
- Add comments for complex logic or explanations of design decisions.
- Avoid unnecessary comments for self-explanatory code.