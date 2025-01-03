precision mediump float;

uniform sampler2D uTexture;

varying vec2 vTexCoord;

void main() {
  vec2 uv = vTexCoord;
  vec4 tex = texture2D(uTexture, uv);
  gl_FragColor = tex;
}