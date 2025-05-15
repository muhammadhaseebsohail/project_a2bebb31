Firstly, you need to install the necessary testing libraries with npm:

```bash
npm install --save-dev jest @testing-library/react @testing-library/user-event axios-mock-adapter
```

Here's how you can write comprehensive unit tests using Jest and React Testing Library:

```jsx
import React from 'react';
import { render, fireEvent, waitFor, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import AxiosMock from 'axios-mock-adapter';
import axios from 'axios';
import FormSubmission from './FormSubmission';

// Create Axios Mock
let mock = new AxiosMock(axios);

describe('FormSubmission', () => {
  afterEach(() => {
    mock.reset();
  });

  it('renders without crashing', () => {
    const { getByText } = render(<FormSubmission url="/test" />);
    expect(getByText('Submit')).toBeInTheDocument();
  });

  it('shows loading state on submit', async () => {
    mock.onPost('/test').reply(200, { data: 'Success' });

    render(<FormSubmission url="/test" />);

    userEvent.type(screen.getByRole('textbox'), 'test');
    userEvent.click(screen.getByText('Submit'));

    expect(screen.getByText('Loading...')).toBeInTheDocument();

    await waitFor(() => expect(screen.queryByText('Loading...')).toBeNull());
  });

  it('shows error message on failure', async () => {
    mock.onPost('/test').networkError();

    render(<FormSubmission url="/test" />);

    userEvent.type(screen.getByRole('textbox'), 'test');
    userEvent.click(screen.getByText('Submit'));

    await waitFor(() => expect(screen.getByText(/^Error: /)).toBeInTheDocument());
  });

  it('clears the input field after successful submission', async () => {
    mock.onPost('/test').reply(200, { data: 'Success' });

    render(<FormSubmission url="/test" />);

    const input = screen.getByRole('textbox');
    userEvent.type(input, 'test');
    userEvent.click(screen.getByText('Submit'));

    await waitFor(() => expect(input).toHaveValue(''));
  });
});
```

This test suite includes tests for:
- Component rendering, ensured by checking if the 'Submit' button is in the document.
- User interactions, by simulating typing and clicking events.
- Edge cases, such as loading state, error messages, and clearing of the input field after successful submission.

For the HTTP request, we're mocking axios with `axios-mock-adapter` to simulate different server responses. This allows us to test how the component handles success and failure without making actual HTTP requests. 

The test suite also uses `waitFor` function from React Testing Library, to handle the asynchronous nature of the axios request and state updates in the component.

This test suite doesn't check props validation because PropTypes is a runtime type checker, and it doesn't throw errors that could be caught in a test. Instead, it logs warnings in the console when the props don't match the expected types. To check props types during testing, you could consider using TypeScript or a similar tool that provides compile-time type checking.