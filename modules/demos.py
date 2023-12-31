import numpy as np
import moderngl
import modules.glmath as glmath
import pygame.image as pgimage
from modules.light import Light


class HelloTriangle:
    def __init__(self, engine) -> None:
        self._gl_context = engine.gl_context
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('default')
        self._vao = self.get_vao()

    def render(self) -> None:
        self._vao.render()

    def destroy(self) -> None:
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()

    def get_vertex_data(self) -> np.ndarray:
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)] 
        vertex_data = np.array(vertex_data, dtype='f4') # 32-bit floating-point
        return vertex_data

    """ 
    Create a Vertex Array Object, an OpenGL Object that stores the format of the vertex data as well as the Buffer Objects.
    Here we specify that the vao contains a vbo that made up of bundles of 3 consecutive 32-bit floats named collectively 'in_position'.
    Buffer objects contain your vertex data. Vertex array objects tell OpenGL how to interpret that data. 
    Without the VAO, OpenGL just knows that you suck some bytes into some buffers. 
    """
    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, [(self._vbo, '3f', 'in_position')])
        return vao

    """ 
    Create a Vertex Buffer Object (a memory buffer in the high speed memory of the GPU) 
    to send information about vertices from the CPU.
    """
    def get_vbo(self) -> moderngl.Buffer:
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name) -> moderngl.Program:
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self._gl_context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program


class TestCube:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._gl_context = engine.gl_context
        # colored cube
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('color_gradiant')
        self._vao = self.get_vao()
        # model matrix 
        self._model_matrix = self.get_identity_matrix() # translations, rotations or scaling applied to the object
        # send transformation matrices to the CPU
        self._shader_program['projection_matrix'].write(self.engine.camera.projection_matrix)
        self._shader_program['view_matrix'].write(self.engine.camera.view_matrix)
        self._shader_program['model_matrix'].write(self._model_matrix)
        
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    def update(self) -> None:
        self._model_matrix = glmath.rotate(self._model_matrix, 0.02, glmath.vec3f(0, 1, 0))
        # update the position of the model
        self._shader_program['model_matrix'].write(self._model_matrix)
        # update the position of the camera
        self._shader_program['view_matrix'].write(self.engine.camera.view_matrix)

    def render(self) -> None:
        self.update()
        self._vao.render()

    def destroy(self) -> None:
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()

    def get_vertex_data(self) -> np.ndarray:
        vertex = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                  (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        surfaces = [(0, 2, 3), (0, 1, 2),
                    (1, 7, 2), (1, 6, 7),
                    (6, 5, 4), (4, 7, 6),
                    (3, 4, 5), (3, 5, 0),
                    (3, 7, 4), (3, 2, 7),
                    (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_vertices_from_surface(vertex, surfaces) # 32-bit floating-point
        
        vertex_color = [(0, 1, 1), (0, 0, 1), (0, 0, 0), (0, 1, 0),
                      (1, 1, 0), (1, 1, 1), (1, 0, 1), (1, 0, 0)]
        
        vertex_color_data = self.get_vertices_from_surface(vertex_color, surfaces) # 32-bit floating-point
        
        vertex_data = np.hstack([vertex_color_data, vertex_data])
        return vertex_data

    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')
    
    @staticmethod
    def get_identity_matrix() -> glmath.mat4x4f:
        return glmath.identity_matrix(glmath.mat4x4f)

    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, 
                                            [(self._vbo, '3f 3f', 'in_color', 'in_position')])
        return vao
        
    def get_vbo(self) -> moderngl.Buffer:
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name) -> moderngl.Program:
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self._gl_context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    
class SkeletonCube:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._gl_context = engine.gl_context
        # colored cube
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('outline')
        self._vao = self.get_vao()
        # model matrix 
        self._model_matrix = self.get_identity_matrix() # translations, rotations or scaling applied to the object
        # send transformation matrices to the CPU
        self._shader_program['projection_matrix'].write(self.engine.camera.projection_matrix)
        self._shader_program['view_matrix'].write(self.engine.camera.view_matrix)
        self._shader_program['model_matrix'].write(self._model_matrix)
        
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    def update(self) -> None:
        self._model_matrix = glmath.rotate(self._model_matrix, 0.02, glmath.vec3f(0, 1, 0))
        # update the position of the model
        self._shader_program['model_matrix'].write(self._model_matrix)
        # update the position of the camera
        self._shader_program['view_matrix'].write(self.engine.camera.view_matrix)

    def render(self) -> None:
        self.update()
        self._vao.render(moderngl.LINE_STRIP)

    def destroy(self) -> None:
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()

    def get_vertex_data(self) -> np.ndarray:
        vertex = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                  (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        lines = [(0, 1), (1, 2), (2, 3), 
                 (3, 0), (0, 5), (5, 4), 
                 (4, 3), (3, 2), (2, 7), 
                 (7, 4), (4, 5), (5, 6),
                 (6, 1), (1, 6), (6, 7)]
        
        vertex_data = self.get_vertices_from_surface(vertex, lines) # 32-bit floating-point
        return vertex_data

    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')
    
    @staticmethod
    def get_identity_matrix() -> glmath.mat4x4f:
        return glmath.identity_matrix(glmath.mat4x4f)

    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, 
                                            [(self._vbo, '3f', 'in_position')])
        return vao
        
    def get_vbo(self) -> moderngl.Buffer:
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name) -> moderngl.Program:
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self._gl_context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    

class CompanionCube:
    def __init__(self, engine) -> None:
        self._engine = engine
        self._light = Light()
        self._gl_context = engine.gl_context
        # companion cube
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('companionCube')
        self._vao = self.get_vao()
        # model matrix 
        self._model_matrix = self.get_identity_matrix() # translations, rotations or scaling applied to the object
        # light
        self.shader_program['light.position'].write(self._light._position)
        self.shader_program['light.color'].write(self._light._color)
        self.shader_program['light.ambient_intensity'].write(self._light._ambient_intensity)
        self.shader_program['light.diffuse_intensity'].write(self._light._diffuse_intensity)
        self.shader_program['light.specular_intensity'].write(self._light._specular_intensity)
        # material
        self._shader_program['surface_brightness'] = 56.0 # shiny
        # texture
        self._texture = self.get_texture(path='textures/companion_cube.png')
        self._shader_program['utexture'] = 0 # Define the texture unit we'll use
        self._texture.use()
        # send transformation matrices to the CPU
        self._shader_program['projection_matrix'].write(self._engine.camera.projection_matrix)
        self._shader_program['view_matrix'].write(self._engine.camera.view_matrix)
        self._shader_program['model_matrix'].write(self._model_matrix)
        
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    def get_texture(self, path: str) -> moderngl.Texture:
        raw_pic = pgimage.load(path).convert()
        size = raw_pic.get_size()
        texture_data = pgimage.tostring(raw_pic, 'RGB')
        texture = self._gl_context.texture(size = size, 
                                           components = 3, 
                                           data = texture_data)
        return texture
    
    def update(self):
        self._model_matrix *= glmath.rotate(0.02, glmath.vec3f(0, 1, 0))
        # update the position of the model
        self._shader_program['model_matrix'].write(self._model_matrix)
        # update the position of the camera
        self._shader_program['view_matrix'].write(self._engine.camera.view_matrix)
        self._shader_program['camera_position'].write(self._engine.camera.position)

    def render(self) -> None:
        self.update()
        self._vao.render()

    def destroy(self) -> None:
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()

    def get_vertex_data(self) -> np.ndarray:
        vertex = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                  (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]

        surfaces = [(0, 2, 3), (0, 1, 2),
                    (1, 7, 2), (1, 6, 7),
                    (6, 5, 4), (4, 7, 6),
                    (3, 4, 5), (3, 5, 0),
                    (3, 7, 4), (3, 2, 7),
                    (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_vertices_from_surface(vertex, surfaces) # 32-bit floating-point
        
        tex_coord =  ((0, 0), (1, 0), (1, 1), (0, 1))
        
        tex_coord_indices = [(0, 2, 3), (0, 1, 2), 
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        
        tex_coord_data = self.get_vertices_from_surface(tex_coord, tex_coord_indices)
        
        normals = [(0, 0, 1) * 6, # 3 triangles per face means 6 vertices with the same normal
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        
        normals_data = np.array(normals, dtype='f4').reshape(36, 3)
        vertex_data = np.hstack([normals_data, vertex_data])
        
        vertex_data = np.hstack([tex_coord_data, vertex_data])
        
        return vertex_data

    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')
    
    @staticmethod
    def get_identity_matrix() -> glmath.mat4x4f:
        return glmath.identity_matrix(glmath.mat4x4f)

    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, 
                                            [(self._vbo, '2f 3f 3f', 'in_texcoord', 'in_normal', 'in_position')])
        return vao
        
    def get_vbo(self) -> moderngl.Buffer:
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name) -> moderngl.Program:
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
        program = self._gl_context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
