import numpy as np
import moderngl


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
        vao = self._gl_context.vertex_array(self._shader_program, [(self._vbo, '3f', 'position')])
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
        self._gl_context = engine.gl_context
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('color_gradiant')
        self._vao = self.get_vao()
        # send transformation matrices to the CPU
        self._shader_program['projection_matrix'].write(engine.camera.projection_matrix)
        self._shader_program['view_matrix'].write(engine.camera.view_matrix)
        
    @property
    def shader_program(self) -> moderngl.Program:
        return self._shader_program

    def render(self) -> None:
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

        vertex_data = self.get_vertices_from_surface(vertex, surfaces)  # 32-bit floating-point
        return vertex_data

    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')

    def get_vao(self) -> moderngl.VertexArray:
        vao = self._gl_context.vertex_array(self._shader_program, [(self._vbo, '3f', 'position')])
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
