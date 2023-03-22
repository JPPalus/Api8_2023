import platform
import pyglet
import pyglet.window as pgwindow
import pyglet.clock as pgclock
import moderngl


if platform.system() == "Darwin":
    pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False


class GLEngine:
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
        self._scene = None
        
    def get_gl_context(self):
        return self._gl_context
    
    def set_scene(self, scene):
        self._scene = scene
        
    def render(self, dt):
        # clear the framebuffer
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior."
        if self._scene:
            # render scene
            self._scene.render()
            # swap buffers
            self._window.flip()
    
    def run(self):
        pyglet.app.run()
        
    def on_close(self):
        if self._scene:
            self._scene.destroy()