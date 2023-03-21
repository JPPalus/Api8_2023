import platform
import pyglet
import pyglet.window as pgwindow
import pyglet.clock as pgclock
import moderngl
import numpy as np


if platform.system() == "Darwin":
    pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False


class HelloTriangle:
    def __init__(self, gl_context):
        self._gl_context = gl_context
        self._vbo = self.get_vbo()
        self._shader_program = self.get_shader_program('default')  
        self._vao = self.get_vao()
        
    def render(self):
        self._vao.render()
        
    def destroy(self):
        self._vbo.release()
        self._shader_program.release()
        self._vao.release()
        
    def get_vertex_data(self):
        vertex_data = [(-0.6, -0.8, 0.0), (0.6, -0.8, 0.0), (0.0, 0.8, 0.0)]
        vertex_data = np.array(vertex_data, dtype = 'f4') # 32-bit floating-point
        return vertex_data
    
    """ 
    Create a Vertex Array Object, an OpenGL Object that stores the format of the vertex data as well as the Buffer Objects.
    Here we specify that the vao contains a vbo that made up of bundles of 3 consecutive 32-bit floats named collectively 'in_position'.
    Buffer objects contain your vertex data. Vertex array objects tell OpenGL how to interpret that data. 
    Without the VAO, OpenGL just knows that you suck some bytes into some buffers. 
    """
    def get_vao(self):
        vao = self._gl_context.vertex_array(self._shader_program, [(self._vbo, '3f', 'in_position')])
        return vao
    
    """ 
    Create a Vertex Buffer Object (a memory buffer in the high speed memory of the GPU) 
    to send information about vertices from the CPU.
    """
    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self._gl_context.buffer(vertex_data)
        return vbo
    
    def get_shader_program(self, shader_name):
        with open(f'shaders/{shader_name}.vert') as file:
            vertex_shader = file.read()
            
        with open(f'shaders/{shader_name}.frag') as file:
            fragment_shader = file.read()
            
        program = self._gl_context.program(vertex_shader = vertex_shader, fragment_shader = fragment_shader)
        return program



class Api8:
    def __init__(self, win_size = (1280, 720), fps = 60):
        # init pyglet and OpenGL context
        self.WIN_SIZE = win_size
        self._window = pgwindow.Window()
        self._window_context = self._window.context
        self._gl_config = self._window_context.config
        self._gl_config.double_buffer = True
        self._gl_config.depth_size = 24
        # loop handler 
        pgclock.schedule_interval(self.render, 1 / fps)
        # detect and use existing OpenGL context
        self._gl_context = moderngl.create_context()
        # scene
        self._scene = HelloTriangle(self._gl_context)
        
    def render(self, dt):
        # clear the framebuffer
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior."
        # render scene
        self._scene.render()
        # swap buffers
        self._window.flip()
    
    def run(self):
        pyglet.app.run()
        
    def on_close(self):
        self._scene.destroy()
    

if __name__ == '__main__':
    demo = Api8()
    demo.run()
