Here's a simple component that displays the task and its requirements:

```jsx
import React from 'react';
import PropTypes from 'prop-types';
import './Task.css';

/**
 * Task Component
 * 
 * This component displays a task with its requirements
 * 
 * @param {Object} props Component props
 * @param {string} props.task The task to be displayed
 * @param {string[]} props.requirements The requirements of the task
 */
const Task = ({ task, requirements }) => {
  // Check if the task or requirements are not provided
  if (!task || !requirements) {
    return <div>Loading...</div>;
  }

  // Check if there is an error in the requirements
  if (!Array.isArray(requirements)) {
    return <div>Error: Invalid requirements</div>;
  }

  return (
    <div className="task">
      <h2>{task}</h2>
      <ul>
        {requirements.map((requirement, index) => (
          <li key={index}>{requirement}</li>
        ))}
      </ul>
    </div>
  );
};

Task.propTypes = {
  task: PropTypes.string.isRequired,
  requirements: PropTypes.arrayOf(PropTypes.string).isRequired,
};

export default Task;
```

Here's the CSS for the component:

```css
/* Task.css */

.task {
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 4px;
  margin-bottom: 20px;
  background-color: #f9f9f9;
}

.task h2 {
  margin: 0 0 10px 0;
  font-size: 20px;
}

.task ul {
  list-style-type: none;
  padding: 0;
}

.task ul li {
  margin-bottom: 5px;
}
```

In this component, we have a functional component named `Task` that accepts `task` and `requirements` as props. It checks if the data is loading or if there is an error, and then maps over the `requirements` array to display each requirement in a list. The `Task` component also uses PropTypes to validate the props. The CSS provides some basic styling for the task and its requirements.