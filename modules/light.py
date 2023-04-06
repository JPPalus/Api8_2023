import modules.glmath as glmath

class Light:
    def __init__(self, position: tuple[float, float, float] = (3, 3, 3), color: tuple[float, float, float] = (1, 1, 1)) -> None:
        self._position = glmath.vec3f(position)
        self._color = glmath.vec3f(color)
        # intensity of lightsources
        self._ambient_intensity: glmath.vec3f = 0.1 * self._color # ambiant
        self._diffuse_intensity: glmath.vec3f = 0.8 * self._color # diffuse
        self._specular_intensity: glmath.vec3f = 1.0 * self._color # specular
        
    @property
    def color(self) -> glmath.vec3f:
        return self._color
    
    @property
    def position(self) -> glmath.vec3f:
        return self._position
    
    @property
    def ambient_intensity(self) -> glmath.vec3f:
        return self._ambient_intensity

    @property
    def diffuse_intensity(self)-> glmath.vec3f:
        return self._diffuse_intensity
    
    @property
    def specular_intensity(self)-> glmath.vec3f:
        return self._specular_intensity
    
    def set_position(self, position: tuple[float, float, float]) -> None:
        self._position = glmath.vec3f(position)
        
    