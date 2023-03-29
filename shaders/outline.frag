//FRAGMENT SHADER
#version 410 core

out vec4 fragColor;

void
main() {
    vec3 color = vec3(0, 0, 0);
    fragColor = vec4(color, 1.0);
}