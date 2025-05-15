Here's an example of how you might create this component using functional components, hooks, and CSS-in-JS. 

1. The complete component code with all imports

```jsx
import React, { useState, useEffect } from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';

/**
 * This component displays a success message after a user successfully logs in.
 * 
 * @component
 * @param {object} props - The component props
 * @param {boolean} props.isLoggedIn - Whether the user is logged in
 * @returns {JSX.Element} The rendered JSX element
 */
function LoginSuccessNotification({ isLoggedIn }) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isLoggedIn) {
      setIsVisible(true);
      const timer = setTimeout(() => setIsVisible(false), 3000);
      return () => clearTimeout(timer);
    }
  }, [isLoggedIn]);

  if (!isVisible) {
    return null;
  }

  return (
    <SuccessNotification>
      You have successfully logged in!
    </SuccessNotification>
  );
}

export default LoginSuccessNotification;
```

2. Any necessary CSS/styling

```jsx
const SuccessNotification = styled.div`
  background-color: #dff0d8;
  color: #3c763d;
  margin: 10px 0;
  padding: 10px 15px;
  border: 1px solid #d6e9c6;
  border-radius: 4px;
  text-align: center;
`;
```

3. PropTypes or TypeScript interfaces

```jsx
LoginSuccessNotification.propTypes = {
  isLoggedIn: PropTypes.bool.isRequired,
};
```

4. Export statements

```jsx
export default LoginSuccessNotification;
```

In this example, the component uses the useEffect hook to set up a timer that makes the success message visible for 3 seconds when the user logs in. The styled-components library is used to add CSS to the success message. PropTypes are used to enforce that the isLoggedIn prop is a boolean.