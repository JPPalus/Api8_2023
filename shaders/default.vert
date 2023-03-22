#version 410 core

in vec3 position;

out vec4 color;

void
main() {
    color = vec4(position, 1.0);
    gl_Position = vec4(position, 1.0);
}