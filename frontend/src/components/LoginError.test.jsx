Here are comprehensive unit tests for the LoginError component:

```jsx
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import LoginError from './LoginError';

describe('LoginError component', () => {
  test('renders without crashing', () => {
    const { getByText } = render(<LoginError message="Test Error" />);
    expect(getByText('Test Error')).toBeInTheDocument();
  });

  test('is dismissible', () => {
    const { getByText, queryByText } = render(<LoginError message="Test Error" />);
    const button = getByText('Dismiss');
    fireEvent.click(button);
    expect(queryByText('Test Error')).toBeNull();
  });

  test('shows error message from props', () => {
    const { getByText } = render(<LoginError message="Test Error 123" />);
    expect(getByText('Test Error 123')).toBeInTheDocument();
  });

  test('does not render when message prop is empty', () => {
    const { queryByText } = render(<LoginError message="" />);
    expect(queryByText('')).toBeNull();
  });
});

describe('LoginError prop types', () => {
  test('throws error on incorrect prop type', () => {
   const spy = jest.spyOn(global.console, 'error');
   render(<LoginError message={123} />);
   expect(spy).toHaveBeenCalled();
  });
});
```

This suite of tests checks:
- The component renders without crashing.
- The component is dismissible by clicking the 'Dismiss' button, which causes the error message to disappear.
- The component correctly displays the error message passed in props.
- The component does not render when the 'message' prop is empty.
- The component logs an error when the prop type for 'message' is incorrect.

The `render` function from 'react-testing-library' is used to render the component, `getByText` and `queryByText` to assert that certain text is in the document, and `fireEvent` to simulate user interactions. The `jest.spyOn` function is used to spy on console.error and check if it was called (indicating a prop types error).