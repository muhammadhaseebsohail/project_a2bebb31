Sure, here's how you might write unit tests for the LoginSuccessNotification component using Jest and React Testing Library.

```jsx
import React from 'react';
import { render, cleanup, act } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import LoginSuccessNotification from './LoginSuccessNotification'; // assuming the path to the component

// cleanup after each test
afterEach(cleanup);

describe('LoginSuccessNotification', () => {
  it('renders without crashing', () => {
    render(<LoginSuccessNotification isLoggedIn={false} />);
  });

  it('does not render when isLoggedIn is false', () => {
    const { queryByText } = render(<LoginSuccessNotification isLoggedIn={false} />);
    expect(queryByText('You have successfully logged in!')).toBeNull();
  });

  it('renders when isLoggedIn is true', () => {
    const { getByText } = render(<LoginSuccessNotification isLoggedIn={true} />);
    expect(getByText('You have successfully logged in!')).toBeInTheDocument();
  });

  it('disappears after 3 seconds when isLoggedIn is true', async () => {
    jest.useFakeTimers();
    const { queryByText } = render(<LoginSuccessNotification isLoggedIn={true} />);
    expect(queryByText('You have successfully logged in!')).toBeInTheDocument();

    act(() => {
      jest.advanceTimersByTime(3000);
    });

    expect(queryByText('You have successfully logged in!')).toBeNull();
    jest.useRealTimers();
  });

  it('throws an error when isLoggedIn prop is not provided', () => {
    console.error = jest.fn();
    render(<LoginSuccessNotification />);
    expect(console.error).toBeCalled();
  });
});
```

In this test suite:

- The "renders without crashing" test verifies that the LoginSuccessNotification component can be rendered without throwing.
- The "does not render when isLoggedIn is false" test checks that the notification does not appear when the user is not logged in.
- The "renders when isLoggedIn is true" test checks that the success message does appear when the user is logged in.
- The "disappears after 3 seconds when isLoggedIn is true" test checks that the success message disappears after 3 seconds when the user is logged in.
- The "throws an error when isLoggedIn prop is not provided" test checks that an error is thrown when the isLoggedIn prop is not provided, which should never happen in production, but is good to check anyway.