export default function sketch(p) {
  let theShader;
  let img;
  let rotX = 0;
  let rotY = 0;
  let translateZ = 0;
  let isMouseOverCanvas = false; // Default to false

  p.preload = () => {
    theShader = p.loadShader(
      '/vertex.glsl',
      '/fragment.glsl'
    );
  };

  p.setup = () => {
    p.createCanvas(600, 600, p.WEBGL);
    p.noStroke();
  };

  p.draw = () => {
    p.background(0);
    
    if (img) {
      p.shader(theShader);
      
      p.push();
      p.rotateX(rotX);
      p.rotateY(rotY);
      p.translate(0, 0, translateZ);
      
      theShader.setUniform('uProjectionMatrix', p._renderer.uPMatrix.mat4);
      theShader.setUniform('uModelViewMatrix', p._renderer.uMVMatrix.mat4);
      theShader.setUniform('uTexture', img);
      
      p.plane(img.width, img.height);
      p.pop();
    }
  };

  p.updateImage = (newImage) => {
    img = newImage;
    p.resizeCanvas(img.width, img.height);
    rotX = 0;
    rotY = 0;
    translateZ = 0;
  };

  p.mouseDragged = (event) => {
    if (isMouseOverCanvas) {
      event.preventDefault(); // Prevent default behavior
      if (p.mouseButton === p.LEFT) {
        rotY += (p.mouseX - p.pmouseX) * 0.01;
        rotX += (p.mouseY - p.pmouseY) * 0.01;
      } else if (p.mouseButton === p.RIGHT) {
        translateZ += (p.mouseY - p.pmouseY);
      }
    }
  };

  p.mouseWheel = (event) => {
    if (isMouseOverCanvas) {
      event.preventDefault(); // Prevent default behavior
      translateZ += event.delta;
    }
  };

  // Function to set the mouse over state
  p.setMouseOverCanvas = (state) => {
    isMouseOverCanvas = state;
  };
}