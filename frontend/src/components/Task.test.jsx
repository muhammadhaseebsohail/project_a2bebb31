In order to test the `Task` component, we will use Jest and the React Testing Library, which are the recommended tools for testing React components. We will need to test the rendering of the component, the user interactions, the prop validation, and the edge cases.

Here's the test file:

```jsx
import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom/extend-expect';
import Task from './Task';

describe('Task', () => {
  it('renders without crashing', () => {
    render(<Task task="Test task" requirements={["Requirement 1", "Requirement 2"]} />);
    expect(screen.getByText('Test task')).toBeInTheDocument();
  });

  it('displays all requirements', () => {
    render(<Task task="Test task" requirements={["Requirement 1", "Requirement 2"]} />);
    expect(screen.getByText('Requirement 1')).toBeInTheDocument();
    expect(screen.getByText('Requirement 2')).toBeInTheDocument();
  });

  it('shows loading state when task or requirements are not provided', () => {
    render(<Task />);
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('shows error state when requirements prop is not an array', () => {
    console.error = jest.fn(); // Suppress console error for this test
    render(<Task task="Test task" requirements={"Invalid requirements"} />);
    expect(screen.getByText('Error: Invalid requirements')).toBeInTheDocument();
    expect(console.error).toHaveBeenCalled();
  });

  it('does not show task if it is not provided', () => {
    render(<Task requirements={["Requirement 1", "Requirement 2"]} />);
    expect(screen.queryByText('Test task')).toBeNull();
  });
});
```

In this test file, we have five tests:

1. "renders without crashing": This test checks if the component renders without throwing any error. It renders the `Task` component with a test task and some requirements and then checks if the task is present in the document.

2. "displays all requirements": This test checks if all the requirements are displayed correctly. It renders the `Task` component with a test task and some requirements and then checks if each requirement is present in the document.

3. "shows loading state when task or requirements are not provided": This test checks the loading state of the component. It renders the `Task` component without any props and then checks if the loading message is present in the document.

4. "shows error state when requirements prop is not an array": This test checks the error state of the component. It renders the `Task` component with a test task and invalid requirements (a string instead of an array) and then checks if the error message is present in the document. It also checks if a console error was printed, which is the expected behavior when the PropTypes validation fails.

5. "does not show task if it is not provided": This test checks if the task is not displayed when it is not provided. It renders the `Task` component with some requirements but without a task and then checks if the test task is not present in the document.