import glm

FOV = 50 # deg
NEAR = 0.1
FAR = 100

class Camera:
    def __init__(self, win_size) -> None:
        self._aspect_ratio = win_size[0] / win_size[1]
        self._position = glm.vec3(0) # eye, position of the camera
        self._center = glm.vec3(0) # the point where the camera aims
        self._up = glm.vec3(0) # how the camera is oriented
        # view matrix : moves your geometry from world space to view space
        self._view_matrix = self.get_identity_matrix()
        # projection matrix : scale the gometry according to the distance from the camera
        self._projection_matrix = self.get_identity_matrix()
        
    @property
    def projection_matrix(self) -> glm.fmat4x4:
        return self._projection_matrix
    
    @property
    def view_matrix(self) -> glm.fmat4x4:
        return self._view_matrix
        
    def get_identity_matrix(self) -> glm.fmat4x4:
        return glm.identity(glm.fmat4x4)
        
    def get_default_projection_matrix(self) -> glm.fmat4x4:
        return glm.perspective(glm.radians(FOV), self._aspect_ratio, NEAR, FAR)
    
    def get_default_view_matrix(self) -> glm.fmat4x4:
        return glm.lookAt(self._position, self._center, self._up)
    
    def set_null_camera(self) -> None:
        self.view_matrix = self.get_identity_matrix()
        self._projection_matrix = self.get_identity_matrix()
    
    def set_default_camera(self) -> None:
        self._projection_matrix = self.get_default_projection_matrix()
        self._position = glm.vec3(2, 3, 3)
        self._up = glm.vec3(0, 1, 0)
        self._view_matrix = self.get_default_view_matrix()