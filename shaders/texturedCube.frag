//FRAGMENT SHADER
#version 410 core

struct Light {
    vec3 position;
    vec3 color;
    vec3 ambient_intensity;
    vec3 diffuse_intensity;
    vec3 specular_intensity;
};

struct Material {
    float surface_brightness;
    vec3 ambient_incidence;
    vec3 diffuse_incidence;
    vec3 specular_incidence;
};

in vec2 vtexcoord;
in vec3 vnormal;
in vec3 vfragment_position;

uniform sampler2D utexture;
uniform vec3 camera_position;
uniform Light light;
uniform Material material;

out vec4 fragColor;


// We could do these operations in the fragment shader but for optimisation purpose it is cleverer to do it in the fragment shader.
// There is a lot more fragments than vertices.
vec3 
getLight(vec3 color) {
    vec3 normal = normalize(vnormal);

    /* ambient light */
    vec3 ambient_light = light.ambient_intensity * light.color * material.ambient_incidence;

    /* diffuse light */
    // The light's direction vector is the difference vector between the light's position vector and the fragment's position vector.
    // We only care about the direction of the light, not its magnitude ; 
    // So all the calculations are done with unit vectors since it simplifies most calculations (like the dot product).
    vec3 light_direction = normalize(light.position - vfragment_position);
    // Next we need to calculate the diffuse impact of the light on the current fragment.
    // We do that by taking the dot product between the normal and light's direction vectors. 
    // The resulting value is then multiplied with the light's color to get the diffuse component, 
    // resulting in a darker diffuse component the greater the angle between both vectors: 
    // If the angle between both vectors is greater than 90 degrees then the result of the dot product will actually become negative,
    // so we max the diffusion to 0 to make sure the diffuse component (and thus the colors) never become negative.
    float diffusion= max(0.0, dot(light_direction, normal));
    vec3 diffuse_light = diffusion * light.diffuse_intensity * light.color * material.diffuse_incidence;

    /* specular light */
    // Specular lighting is based on the reflective properties of surfaces.
    // We calculate a reflection vector by reflecting the light direction around the normal vector. 
    // Then we calculate the angular distance between this reflection vector and the view direction, 
    // the closer the angle between them, the greater the impact of the specular light.
    // We do the lighting calculations in view space so that the viewer's position is always at (0,0,0).
    // First we calculate the the view direction vector.
    vec3 view_direction = normalize(camera_position - vfragment_position);
    // Then the corresponding reflect vector along the normal axis.
    // The reflect function expects the first vector to point from the light source towards the fragment's position,
    // so it's the oposite of the light's direction
    vec3 reflection_direction = reflect(-light_direction, normal);
    // Then what's left to do is to actually calculate the specular component.
    // We first calculate the dot product between the view direction and the reflect direction (and make sure it's not negative).
    // Then raise it to the power of the britghness of the surface material.
    // The higher the shininess value of an object, the more it properly reflects the light instead of scattering it all around and thus the smaller the highlight becomes. 
    float specular = pow(max(dot(view_direction, reflection_direction), 0), material.surface_brightness);
    vec3 specular_light = specular * light.specular_intensity * light.color * material.specular_incidence;

    return color * (ambient_light + diffuse_light + specular_light);
}

void
main() {
    vec3 color = texture(utexture, vtexcoord).rgb;
    color = getLight(color);
    fragColor = vec4(color, 1.0);
}