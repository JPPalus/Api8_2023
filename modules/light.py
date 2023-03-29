import glm

class Light:
    def __init__(self, position: tuple[int, int, int] = (3, 3, -3), color: tuple[int, int, int] = (1, 1, 1)) -> None:
        self._position = glm.vec3(position)
        self._color = glm.vec3(color)
        # intensity of lightsources
        self._ambient_intensity = 0.1 * self._color # ambiant
        self._diffuse_intensity = 0.8 * self._color # diffuse
        self._specular_intensity = 1.0 * self._color # specular
        
        @property
        def color(self) -> glm.fvec3:
            return self._color
        
        @property
        def position(self) -> glm.fvec3:
            return self._position
        
        @property
        def ambient_intensity(self) -> glm.fvec3:
            return self._ambient_intensity

        @property
        def diffuse_intensity(self)-> glm.fvec3:
            return self._diffuse_intensity
        
        @property
        def specular_intensity(self)-> glm.fvec3:
            return self._specular_intensity
        
    