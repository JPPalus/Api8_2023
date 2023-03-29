#version 410 core

layout (quads, equal_spacing, ccw) in;

float
B(int i, float u) {
    // Binomial coefficient lookup table
    const vec4 bc = vec4(1, 3, 3, 1);
    return bc[i] * pow(u, i) * pow(1.0 - u, 3 - i);
}

void 
main() {
    vec4 p = vec4(1.0);

    float u = gl_TessCoord.x;
    float v = gl_TessCoord.y;
    
    for (int j = 0; j < 4; ++j) {
        for (int i = 0; i < 4; ++i) {
            p += B(i, u) * B(j, v) * gl_in[4*j+i].gl_Position;
        }
    }
    
    gl_Position = p;
}