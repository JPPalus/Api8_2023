#version 410 core

in vec2 vtexcoord;

uniform sampler2D utexture;

out vec4 fragColor;

void
main() {
    vec3 color = texture(utexture, vtexcoord).rgb;
    fragColor = vec4(color, 1.0);
}