//VERTEX SHADER
#version 410 core

in vec2 in_texcoord;
in vec3 in_normal;
in vec3 in_position;

uniform mat4 projection_matrix;
uniform mat4 view_matrix;
uniform mat4 model_matrix;

out vec2 vtexcoord;
out vec3 vnormal;
out vec3 vfragment_position;


void
main() {
    vtexcoord = in_texcoord;
    // We're going to do all the lighting calculations in world space so we want a vertex position that is in world space.
    // We can accomplish this by multiplying the vertex position attribute with the model matrix to transform it to world space coordinates. 
    vfragment_position = vec3(model_matrix * vec4(in_position, 1.0));
    // Calculations in the fragment shader are all done in world space so we should transform the normal vectors to world space.
    // But mormal vectors are only direction vectors and do not represent a specific position in space.
    // And normal vectors also do not have a homogeneous coordinate (the w component of a vertex position). 
    // This means that translations should not have any effect on the normal vectors.
    // So if we want to multiply the normal vectors with a model matrix we can either take the upper-left 3x3 matriox of the model matrix,
    // or set the w component of a normal vector to 0.
    // But we now have a non-uniform scale that would make the normal vector not perpendicular to the corresponding surface anymore.
    // To solve that problem we use a "normal matrix", i.e "the transpose of the inverse of the upper-left 3x3 part of the model matrix".
    // (note that a uniform scale only changes the normal's magnitude, not its direction, which is easily fixed by normalizing it).
    // (if you want to understand the linear algebra behind what is called a "normal matrix", read that : http://www.lighthouse3d.com/tutorials/glsl-12-tutorial/the-normal-matrix/)
    vnormal = mat3(transpose(inverse(model_matrix))) * normalize(in_normal);

    gl_Position = projection_matrix * view_matrix * model_matrix * vec4(in_position, 1.0);
}