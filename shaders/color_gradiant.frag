//FRAGMENT SHADER
#version 410 core

in vec4 vcolor;

out vec4 fragColor;

void
main() {
    fragColor = vcolor;
}