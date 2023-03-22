#version 410 core

in vec3 position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;

out vec4 Color;

void
main() {
    Color = vec4(position, 1.0);
    gl_Position = projection_matrix * view_matrix * vec4(position, 1.0);
}