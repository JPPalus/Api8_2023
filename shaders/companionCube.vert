#version 410 core

in vec2 in_texcoord;
in vec3 in_position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

out vec2 vtexcoord;


void
main() {
    vtexcoord = in_texcoord;
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}