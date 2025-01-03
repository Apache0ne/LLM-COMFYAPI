import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Setup from './components/Setup';
import ImageGenerator from './components/ImageGenerator';
import { getLLMSetup } from './api/api';
import './styles/App.css';

function App() {
  const [isSetupComplete, setIsSetupComplete] = useState(false);

  useEffect(() => {
    checkSetup();
  }, []);

  const checkSetup = async () => {
    try {
      const setup = await getLLMSetup();
      setIsSetupComplete(setup.isComplete);
    } catch (error) {
      console.error('Failed to check setup:', error);
    }
  };

  const handleSetupComplete = () => {
    console.log('Setup complete');
    console.log('isSetupComplete set to true');
    setIsSetupComplete(true);
  };

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>ComfyUI Image Generator</h1>
        </header>
        <main>
          <Routes>
            <Route path="/setup" element={<Setup onSetupComplete={handleSetupComplete} />} />
            <Route path="/image-generator" element={isSetupComplete ? <ImageGenerator /> : <Navigate to="/setup" replace />} />
            <Route path="/" element={<Navigate to="/setup" />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;