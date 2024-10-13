#version 450

layout (location = 0) in vec2 vertex;
layout (location = 1) in vec3 color;

layout (location = 0) out vec3 outColor;

void main() {
    gl_Position = vec4(vertex, 0, 1);
    outColor = color;
}
