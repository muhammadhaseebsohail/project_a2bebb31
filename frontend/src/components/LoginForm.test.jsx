Here are the unit tests for the LoginForm component:

```jsx
// Required imports
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LoginForm from './LoginForm';

// Component rendering test
test('LoginForm renders without crashing', () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);
  expect(screen.getByPlaceholderText('Username')).toBeInTheDocument();
  expect(screen.getByPlaceholderText('Password')).toBeInTheDocument();
});

// User interactions test
test('LoginForm handles user input and form submission', () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: 'testUsername' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'testPassword' } });
  fireEvent.click(screen.getByValue('Log In'));

  expect(onSubmit).toHaveBeenCalledWith({ username: 'testUsername', password: 'testPassword' });
});

// Props validation test
test('LoginForm calls onSubmit prop when form is submitted', () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  fireEvent.click(screen.getByValue('Log In'));

  expect(onSubmit).toHaveBeenCalled();
});

// Edge cases test
test('LoginForm displays error message when username or password is missing', () => {
  const onSubmit = jest.fn();
  render(<LoginForm onSubmit={onSubmit} />);

  fireEvent.change(screen.getByPlaceholderText('Username'), { target: { value: '' } });
  fireEvent.change(screen.getByPlaceholderText('Password'), { target: { value: 'testPassword' } });
  fireEvent.click(screen.getByValue('Log In'));

  expect(screen.getByText('Both fields are required')).toBeInTheDocument();
  expect(onSubmit).not.toHaveBeenCalled();
});
```

These tests cover:

- Whether the LoginForm component renders without crashing.
- Whether the component handles user input and form submission correctly.
- Whether the onSubmit prop is called when the form is submitted.
- Edge cases where the username or password is missing, in which case an error message should be displayed and the onSubmit prop should not be called. 

Jest and React Testing Library are used for these tests. The @testing-library/jest-dom/extend-expect library provides custom Jest matchers that you can use to extend Jest's default matchers.