Creating unit tests for a component is not exactly creating a component itself, but I can provide you an example of how a LoginForm component might look like and then create a unit test for it using Jest and React Testing Library.

Here is the LoginForm component:

```jsx
// LoginForm.js
import React, { useState } from 'react';
import PropTypes from 'prop-types';
import './LoginForm.css';

const LoginForm = ({ onSubmit }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = (event) => {
    event.preventDefault();
    onSubmit({ username, password });
  };

  return (
    <form onSubmit={handleSubmit} className="loginForm">
      <input
        type="text"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
        placeholder="Username"
      />
      <input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Password"
      />
      <button type="submit">Login</button>
    </form>
  );
};

LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default LoginForm;
```

Here is the CSS for LoginForm component:

```css
/* LoginForm.css */
.loginForm input {
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.loginForm button {
  padding: 10px 20px;
  border-radius: 5px;
  border: none;
  background-color: #007bff;
  color: white;
  cursor: pointer;
}
```

Here is the LoginForm.test.js file where we test the LoginForm component:

```jsx
// LoginForm.test.js
import React from 'react';
import { render, fireEvent } from '@testing-library/react';
import LoginForm from './LoginForm';

test('calls onSubmit with the username and password when submitted', () => {
  const handleSubmit = jest.fn();
  const { getByPlaceholderText, getByText } = render(
    <LoginForm onSubmit={handleSubmit} />
  );

  fireEvent.change(getByPlaceholderText(/username/i), {
    target: { value: 'testuser' },
  });

  fireEvent.change(getByPlaceholderText(/password/i), {
    target: { value: 'testpass' },
  });

  fireEvent.click(getByText(/login/i));

  expect(handleSubmit).toHaveBeenCalledWith({
    username: 'testuser',
    password: 'testpass',
  });
});

```

In the above test, we're testing whether the LoginForm component calls the onSubmit prop with the correct username and password when the form is submitted.

Note: Remember to install the necessary testing libraries using npm or yarn:

```
npm install --save-dev @testing-library/react jest
```