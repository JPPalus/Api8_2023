import numpy as np
import moderngl
import glm


class Teapot:
    def __init__(self, engine) -> None:
        self.engine = engine
        self._gl_context = engine.gl_context
        # colored cube
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('teapot')
        self._vao = self.get_vao()
        self._gl_context.patch_vertices = 16
        self._gl_context.wireframe = True
        # model matrix 
        self._model_matrix = glm.rotate(0.02, glm.vec3(0, 1, 1))
        # send transformation matrices to the CPU
        self._shader_program['projection_matrix'].write(self.engine.camera.projection_matrix)
        self._shader_program['view_matrix'].write(self.engine.camera.view_matrix)
        self._shader_program['model_matrix'].write(self._model_matrix)
        
        
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program
    
    def update(self):
        self._model_matrix = glm.rotate(self._model_matrix, 0.02, glm.vec3(0, 0, 1))
        self._shader_program['model_matrix'].write(self._model_matrix)

    def render(self) -> None:
        self.update()
        self._vao.render(mode=moderngl.PATCHES)

    def destroy(self) -> None:
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()

    def get_vertex_data(self) -> np.ndarray:
        from beta.teapot_data import vertex_teapot
        vertex = vertex_teapot
        from beta.teapot_data import patches
        surfaces = patches
        
        vertex_data = self.get_vertices_from_surface(vertex, surfaces) # 32-bit floating-point
        
        return vertex_data
    
    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice-1]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')
    
    @staticmethod
    def get_identity_matrix() -> glm.fmat4x4:
        return glm.identity(glm.fmat4x4)

    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, 
                                            [(self._vbo, '3f', 'in_position')])
        return vao
        
    def get_vbo(self) -> moderngl.Buffer:
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo

    def get_shader_program(self, shader_name) -> moderngl.Program:
        with open(f'beta/{shader_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'beta/{shader_name}.frag') as file:
            fragment_shader = file.read()
            
        with open(f'beta/{shader_name}.tecs') as file:
            tessellation_control_shader = file.read()
            
        with open(f'beta/{shader_name}.tess') as file:
            tessellation_evaluation_shader = file.read()

        program = self._gl_context.program(vertex_shader=vertex_shader, 
                                           fragment_shader=fragment_shader,
                                           tess_control_shader=tessellation_control_shader,
                                           tess_evaluation_shader=tessellation_evaluation_shader)
        return program