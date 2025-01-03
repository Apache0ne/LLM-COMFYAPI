import React, { useState } from 'react';
import '../styles/PromptInput.css';

function PromptInput({ onSubmit }) {
  const [prompt, setPrompt] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (prompt.trim()) {
      onSubmit(prompt);
      setPrompt(''); // Clear the input after submission
    }
  };

  return (
    <form onSubmit={handleSubmit} className="prompt-input">
      <textarea
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        placeholder="Enter your prompt here..."
        required
      />
      <button type="submit">Generate Image</button>
    </form>
  );
}

export default PromptInput;