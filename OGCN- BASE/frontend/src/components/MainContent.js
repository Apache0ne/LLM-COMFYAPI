import React, { useRef } from 'react';
import ShaderCanvas from './ShaderCanvas';
import '../styles/MainContent.css';

const MainContent = ({
  isLoading,
  error,
  feedback,
  generatedImage,
  useShaderCanvas,
  setUseShaderCanvas,
  originalPrompt,
  improvedPrompt,
  savedPrompts,
}) => {
  const promptDisplayRef = useRef(null);

  React.useEffect(() => {
    if (promptDisplayRef.current) {
      promptDisplayRef.current.scrollTop = promptDisplayRef.current.scrollHeight;
    }
  }, [originalPrompt, improvedPrompt, savedPrompts]);

  return (
    <div className="main-content">
      {isLoading && <p className="loading-message">Generating image...</p>}
      {error && <p className="error">{error}</p>}
      {feedback && <p className="feedback">{feedback}</p>}

      {generatedImage && (
        <div className="generated-image-container">
          <div className="button-container">
            <button onClick={() => setUseShaderCanvas(!useShaderCanvas)}>
              {useShaderCanvas ? 'Show Regular Image' : 'Show Shader Canvas'}
            </button>
          </div>
          {useShaderCanvas ? (
            <ShaderCanvas imageUrl={generatedImage} />
          ) : (
            <img src={generatedImage} alt="Generated" className="generated-image" />
          )}
        </div>
      )}
    </div>
  );
};

export default MainContent;