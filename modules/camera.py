import glm

FOV = 50 # deg
NEAR = 0.1
FAR = 100
SPEED = 5.

class Camera:
    def __init__(self, win_size) -> None:
        self._aspect_ratio = win_size[0] / win_size[1]
        self._position = glm.vec3(0) # eye, position of the camera
        self._center = glm.vec3(0) # the point where the camera aims
        self._up = glm.vec3(0) # how the camera is oriented
        self._right = glm.vec3(1, 0, 0)
        self._forward = glm.vec3(0, 0, -1)
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
    
    @staticmethod
    def get_identity_matrix() -> glm.fmat4x4:
        return glm.identity(glm.fmat4x4)
    
    def move(self, direction, dt):
        velocity = SPEED * dt
        if direction == 'forward':
            self._position += self._forward * velocity
        if direction == 'backward':
            self._position -= self._forward * velocity
        if direction == 'straf_left':
            self._position -= self._right * velocity
        if direction == 'straf_right':
            self._position += self._right * velocity
        if direction == 'up':
            self._position += self._up * velocity
        if direction == 'down':
            self._position -= self._up * velocity
        if direction == 'left':
            self._position = glm.rotate(self._position, velocity / 10, glm.vec3(0, -1, 0))
        if direction == 'right':
            self._position = glm.rotate(self._position, velocity / 10, glm.vec3(0, 1, 0))
        # update the camera position according to keyboard events
        self.update_view_matrix()
        
    def update_view_matrix(self):
        self._view_matrix = glm.lookAt(self._position, self._position + self._forward, self._up)
    
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