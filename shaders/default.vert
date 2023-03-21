#version 460 core

in vec4 in_position;

void
main() {
    gl_Position = in_position;
}