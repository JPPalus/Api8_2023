
//VERTEX SHADER
#version 410 core

in vec3 in_color;
in vec3 in_position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

out vec4 vcolor;

void
main() {
    vcolor = vec4(in_color, 1.0);
    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}