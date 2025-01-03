import React, { useRef, useEffect, useState } from 'react';
import p5 from 'p5';
import sketch from '../p5setup/sketch';
import '../styles/ShaderCanvas.css';

const ShaderCanvas = ({ imageUrl }) => {
  const canvasRef = useRef(null);
  const [p5Instance, setP5Instance] = useState(null);
  const [isMouseOverCanvas, setIsMouseOverCanvas] = useState(false);

  useEffect(() => {
    if (!p5Instance) {
      const newP5 = new p5(sketch, canvasRef.current);
      setP5Instance(newP5);
    }

    return () => {
      if (p5Instance) {
        p5Instance.remove();
      }
    };
  }, [p5Instance]);

  useEffect(() => {
    if (p5Instance && imageUrl) {
      p5Instance.loadImage(imageUrl, (loadedImg) => {
        p5Instance.updateImage(loadedImg);
      });
    }
  }, [p5Instance, imageUrl]);

  useEffect(() => {
    if (p5Instance) {
      p5Instance.setMouseOverCanvas(isMouseOverCanvas);
    }
  }, [p5Instance, isMouseOverCanvas]);

  useEffect(() => {
    if (canvasRef.current) {
      canvasRef.current.oncontextmenu = (e) => e.preventDefault();
    }
  }, []);

  const handleMouseOver = () => {
    setIsMouseOverCanvas(true);
  };

  const handleMouseOut = () => {
    setIsMouseOverCanvas(false);
  };

  return (
    <div className="shader-canvas-container">
      <div
        ref={canvasRef}
        className="shader-canvas"
        onMouseOver={handleMouseOver}
        onMouseOut={handleMouseOut}
      ></div>
      {!imageUrl && <p className="no-image-message">Please generate an image to apply 3D shader effects.</p>}
    </div>
  );
};

export default ShaderCanvas;