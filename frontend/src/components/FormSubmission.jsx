Here's a simple example of a form submission component using React, Axios for HTTP requests, and Prop-types for prop type checking.

```jsx
import React, { useState } from 'react';
import axios from 'axios';
import PropTypes from 'prop-types';
import styled from 'styled-components';

const FormWrapper = styled.form`
  display: flex;
  flex-direction: column;
  width: 400px;
  margin: auto;
`;

const Input = styled.input`
  margin-bottom: 10px;
  padding: 10px;
  font-size: 16px;
`;

const Button = styled.button`
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  cursor: pointer;
`;

const FormSubmission = ({ url }) => {
  const [inputValue, setInputValue] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);

    try {
      const response = await axios.post(url, { data: inputValue });
      console.log(response.data); // Handle server response here
      setInputValue('');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <FormWrapper onSubmit={handleSubmit}>
      <Input
        type="text"
        value={inputValue}
        onChange={event => setInputValue(event.target.value)}
      />
      <Button type="submit">Submit</Button>
    </FormWrapper>
  );
};

FormSubmission.propTypes = {
  url: PropTypes.string.isRequired,
};

export default FormSubmission;
```

In this component, styled-components is used for CSS-in-JS styling. The form has an input field and a submit button. The input field's value is managed with React's useState hook. The handleSubmit function is responsible for submitting the form data to the back-end. It uses axios to send a POST request with the form data. The loading state is managed with a useState hook, and the error state is managed with another useState hook. The loading and error states are displayed to the user if necessary.

The component also uses PropTypes to enforce that the `url` prop is a string and is required. This helps prevent bugs and makes the component easier to use correctly.