import glm
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
        self._default_position =  glm.vec3(position)
        self._position = copy(self._default_position) # eye, position of the camera
        self._center = glm.vec3(0) # the point where the camera aims
        self._up = glm.vec3(0) # how the camera is oriented
        self._right = glm.vec3(1, 0, 0)
        self._forward = glm.vec3(0, 0, -1)
        self._yaw = yaw # lacet
        self._pitch = pitch # tangage
        # view matrix : moves your geometry from world space to view space
        self._view_matrix = glmath.identity_matrix()
        # projection matrix : scale the gometry according to the distance from the camera
        self._projection_matrix = glmath.identity_matrix()
        
    @property
    def projection_matrix(self) -> glm.fmat4x4:
        return self._projection_matrix
    
    @property
    def view_matrix(self) -> glm.fmat4x4:
        return self._view_matrix
    
    @property
    def default_position(self) -> glm.fvec3:
        return self._default_position
    
    @property
    def position(self) -> glm.fvec3:
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
        # dx = dx if abs(dx) > abs(dy) else 0
        # dy = dy if abs(dy) > abs(dx) else 0
            
        self._yaw += dx * SENSITIVITY
        self._pitch -= dy * SENSITIVITY
        self.update_camera_vectors()
        self.update_view_matrix()
        
    def update_camera_vectors(self) -> None:
        self._pitch = max(-89, min(89, self._pitch))
        yaw = glm.radians(self._yaw)
        pitch = glm.radians(self._pitch)
        
        # forward.x = cos(yaw), forxward.z = sin(yaw)
        # forward.x = cos(pitch), forward.y = sin(pitch), forward.z = cos(pitch)
        self._forward.x = glm.cos(yaw) * glm.cos(pitch)
        self._forward.y = glm.sin(pitch)
        self._forward.z = glm.sin(yaw) * glm.cos(pitch)
        
        self._forward = glm.normalize(self._forward)
        self._right = glm.normalize(glm.cross(self._forward, glm.vec3(0, 1, 0)))
        # self._up = glm.normalize(glm.cross(self._right, self._forward))
        
    def update_view_matrix(self) -> None:
        self._view_matrix = glm.lookAt(self._position, self._position + self._forward, self._up)
    
    def get_default_projection_matrix(self) -> glm.fmat4x4:
        return glm.perspective(glm.radians(FOV), self._aspect_ratio, NEAR, FAR)
    
    def get_default_view_matrix(self) -> glm.fmat4x4:
        return glm.lookAt(self._position, self._center, self._up)
    
    def look_at_scene(self):
        self._view_matrix = glm.lookAt(self._position, self._center, self._up)
    
    def set_null_camera(self) -> None:
        self._position = glm.vec3(0)
        self._center = glm.vec3(0)
        self._up = glm.vec3(0)
        self._yaw = -90 
        self._pitch = 0 
        self.view_matrix = glmath.identity_matrix()
        self._projection_matrix = glmath.identity_matrix()
    
    def set_default_camera(self) -> None:
        self._position = copy(self._default_position)
        self._center = glm.vec3(0)
        self._up = glm.vec3(0, 1, 0)
        self._yaw = -90 
        self._pitch = 0 
        self._view_matrix = self.get_default_view_matrix()
        self._projection_matrix = self.get_default_projection_matrix()
        
    def move_to_position(self, position: tuple[int, int, int]):
        self._position = glm.vec3(position)
        self.update_view_matrix()
        
    def reset_camera(self) -> None:
        self.set_default_camera()
        