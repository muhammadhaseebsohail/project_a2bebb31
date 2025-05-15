Here is a simple login form component built with React and styled-components. It includes input validation and error handling. 

```jsx
// Required Imports
import React, { useState } from 'react'
import PropTypes from 'prop-types'
import styled from 'styled-components'

// Styled Components (CSS in JS)
const Form = styled.form`
  display: flex;
  flex-direction: column;
  width: 300px;
  margin: 0 auto;
`

const Input = styled.input`
  margin-bottom: 10px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ddd;
`

const ErrorMessage = styled.div`
  color: red;
  margin-bottom: 10px;
`

// Login Form Component
const LoginForm = ({ onSubmit }) => {
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState(null)

  const handleSubmit = e => {
    e.preventDefault();
    if(!username || !password) {
      setError('Both fields are required');
    } else {
      setError(null);
      onSubmit({ username, password });
    }
  };

  return (
    <Form onSubmit={handleSubmit}>
      {error && <ErrorMessage>{error}</ErrorMessage>}
      <Input
        type="text"
        value={username}
        onChange={e => setUsername(e.target.value)}
        placeholder="Username"
      />
      <Input
        type="password"
        value={password}
        onChange={e => setPassword(e.target.value)}
        placeholder="Password"
      />
      <Input type="submit" value="Log In" />
    </Form>
  );
};

// PropTypes
LoginForm.propTypes = {
  onSubmit: PropTypes.func.isRequired,
};

export default LoginForm;
```

In this component, we are using React's useState hook to manage the state of the username, password, and error message. The form has an onSubmit event that triggers the handleSubmit function. This function validates the inputs and submits the form if the inputs are valid. If the inputs are not valid, it sets an error message. 

The styled-components library is used here to write CSS in JavaScript. This allows for better component encapsulation and avoids CSS class name clashes. 

The onSubmit prop is typed with PropTypes, and it is expected to be a function. This function will be called with the form data when the form is submitted.