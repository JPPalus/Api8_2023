import modules.glmath as glmath
from copy import copy

FOV = 50 # deg
NEAR = 0.1
FAR = 100
SPEED = 0.008
SENSITIVITY = 0.08

class Camera:
    def __init__(self, engine, position: tuple[float, float, float] = (0, 0, 4), yaw: float = -90, pitch: float = 0.0) -> None:
        self._engine = engine
        self._aspect_ratio = engine.win_size[0] / engine.win_size[1]
        self._default_position =  glmath.vec3f(position)
        self._position = copy(self._default_position) # eye, position of the camera
        self._center = glmath.vec3f(0) # the point where the camera aims
        self._up = glmath.vec3f(0, 1, 0) # how the camera is oriented
        self._right = glmath.vec3f(1, 0, 0)
        self._forward = glmath.vec3f(0, 0, -1)
        self._yaw = yaw # lacet
        self._pitch = pitch # tangage
        # view matrix : moves your geometry from world space to view space
        self._view_matrix = glmath.identity_matrix()
        # projection matrix : scale the gometry according to the distance from the camera
        self._projection_matrix = glmath.identity_matrix()
        
    @property
    def projection_matrix(self) -> glmath.mat4x4f:
        return self._projection_matrix
    
    @property
    def view_matrix(self) -> glmath.mat4x4f:
        return self._view_matrix
    
    @property
    def default_position(self) -> glmath.vec3f:
        return self._default_position
    
    @property
    def position(self) -> glmath.vec3f:
        return self._position
    
    def move(self, direction: str, dt: float) -> None:
        velocity = SPEED * dt
        # movement controls
        if direction == 'forward':
            self._position += self._forward * velocity
        elif direction == 'backward':
            self._position -= self._forward * velocity
        elif direction == 'straf_left':
            self._position -= self._right * velocity
        elif direction == 'straf_right':
            self._position += self._right * velocity
        elif direction == 'straf_up':
            self._position += self._up * velocity
        elif direction == 'straf_down':
            self._position -= self._up * velocity
        elif direction == 'left':
            self._yaw -= SENSITIVITY * 100 * velocity
        elif direction == 'right':
            self._yaw += SENSITIVITY * 100 * velocity
        elif direction == 'up':
            self._pitch -= SENSITIVITY * 100 * velocity
        elif direction == 'down':
            self._pitch += SENSITIVITY * 100 * velocity
        # update the camera position according to keyboard events
        self.update_camera_vectors()
        self.update_view_matrix()
        
    def rotate(self, x: float, y: float, dx: float, dy: float) -> None:
        if self._engine.debug:
            print(f'x = {x}, y = {y}, dx = {dx}, dy = {dy}')
            
        self._yaw += dx * SENSITIVITY
        self._pitch -= dy * SENSITIVITY
        self.update_camera_vectors()
        self.update_view_matrix()
        
    def update_camera_vectors(self) -> None:
        self._pitch = max(-89, min(89, self._pitch))
        yaw = glmath.radians(self._yaw)
        pitch = glmath.radians(self._pitch)
        
        self._forward = glmath.euler_to_3Dvector(yaw, pitch)
        self._forward = glmath.normalize(self._forward)
        self._right = glmath.normalize(glmath.cross(self._forward, glmath.vec3f(0, 1, 0)))
        
    def update_view_matrix(self) -> None:
        self._view_matrix = glmath.lookAt(self._position, self._position + self._forward, self._up)
    
    def get_default_projection_matrix(self) -> glmath.mat4x4f:
        return glmath.perspective(glmath.radians(FOV), self._aspect_ratio, NEAR, FAR)
    
    def get_default_view_matrix(self) -> glmath.mat4x4f:
        return glmath.lookAt(self._position, self._center, self._up)
    
    def look_at_scene(self): # TODO
        self._view_matrix = glmath.lookAt(self._position, self._center, self._up)
    
    def set_null_camera(self) -> None:
        self._position = glmath.vec3f(0)
        self._center = glmath.vec3f(0)
        self._up = glmath.vec3f(0)
        self._yaw = -90 
        self._pitch = 0 
        self.view_matrix = glmath.identity_matrix()
        self._projection_matrix = glmath.identity_matrix()
    
    def set_default_camera(self) -> None:
        self._position = copy(self._default_position)
        self._center = self._position + self._forward
        self._up = glmath.vec3f(0, 1, 0)
        self._yaw = -90 
        self._pitch = 0 
        self._view_matrix = self.get_default_view_matrix()
        self._projection_matrix = self.get_default_projection_matrix()
        
    def set_position(self, position: tuple[int, int, int]):
        self._position = glmath.vec3f(position)
        self._default_position = glmath.vec3f(position)
        self.update_view_matrix()
        
    def move_to_position(self, position: tuple[float, float, float]):
        self._position = glmath.vec3f(position)
        self.update_camera_vectors()
        self.update_view_matrix()
        
    def reset_camera(self) -> None:
        self.set_default_camera()
        self.update_camera_vectors()
        self.update_view_matrix() 