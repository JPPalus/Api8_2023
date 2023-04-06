import glm
from typing import TypeAlias, Any, overload



#-------------- types -------------------#

vec1f: TypeAlias = glm.f32vec1
vec2f: TypeAlias = glm.f32vec2
vec3f: TypeAlias = glm.f32vec3
vec4f: TypeAlias = glm.f32vec4
mat4x4f: TypeAlias = glm.f32mat4x4

#-------------- scalars -----------------#

def radians(angle: float) -> float:
    return glm.radians(angle)

#----------- linear algebrae ------------#

def cross(x: vec3f, y: vec3f) -> vec3f :
    return glm.cross(x, y)

@overload
def normalize(vector: vec1f) -> vec1f:
    ...

@overload
def normalize(vector: vec2f) -> vec2f:
    ...

@overload
def normalize(vector: vec3f) -> vec3f:
    ...

@overload
def normalize(vector: vec4f) -> vec4f:
    ...
    
def normalize(arg0):
    if isinstance(arg0, vec1f):
        return glm.normalize(arg0)
    elif isinstance(arg0, vec2f):
        return glm.normalize(arg0)
    elif isinstance(arg0, vec3f):
        return glm.normalize(arg0)
    elif isinstance(arg0, vec4f):
        return glm.normalize(arg0)
    raise ValueError('Unsupported parameter type')
    
def euler_to_3Dvector(yaw: float, pitch: float) -> vec3f:
    forward = vec3f()
    forward.x = glm.cos(yaw) * glm.cos(pitch)
    forward.y = glm.sin(pitch)
    forward.z = glm.sin(yaw) * glm.cos(pitch)
    return forward

def identity_matrix() -> mat4x4f:
    return glm.identity(mat4x4f)

@overload
def rotate(angle: float, axis: vec3f) -> mat4x4f:
    return glm.rotate(angle = angle, axis = axis)

@overload
def rotate(mat: mat4x4f, angle: float, axis: vec3f) -> mat4x4f:
    return glm.rotate(m = mat, angle = angle, axis = axis)

def rotate(angle: float, axis: vec3f, *args, **kwargs):
    if len(args):
        if isinstance(args[0], mat4x4f):
            return glm.rotate(args[0], angle, axis)   
        raise ValueError('Unsupported parameter type')
    else:
        return glm.rotate(angle, axis)
    

def translate(mat: mat4x4f, vec: vec3f) -> mat4x4f:
    return glm.translate(mat, vec)

def perspective(fovy: float, aspect: float, near: float, far: float) -> mat4x4f:
    return glm.perspective(fovy, aspect, near, far)

def lookAt(eye: vec3f, center: vec3f, up: vec3f) -> mat4x4f:
    return glm.lookAt(eye, center, up)




    

