import platform
import pyglet
import pyglet.window as pgwindow
import pyglet.clock as pgclock
import moderngl
from modules.camera import Camera


if platform.system() == "Darwin":
    pyglet.options["shadow_window"] = False
pyglet.options["debug_gl"] = False

class GLEngine:
    def __init__(self, win_size=(1280, 720), fps=60) -> None:
        # init pyglet and OpenGL context
        self._WIN_SIZE = win_size
        self._window = pgwindow.Window(vsync=False)
        self._window_context = self._window.context
        # keeps track of time
        self._time = 0
        # keyboard event handler
        self._keys = pgwindow.key.KeyStateHandler()
        self._window.push_handlers(self._keys)
        # detect and use existing OpenGL context
        self._gl_context = moderngl.create_context()
        # self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.PROGRAM_POINT_SIZE)
        self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.PROGRAM_POINT_SIZE)
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior."
        # loop handler
        pgclock.schedule(self.update_time)
        pgclock.schedule(self.handle_keys)
        pgclock.schedule_interval(self.render, 1 / fps)
        # camera
        self._camera = Camera(self._WIN_SIZE)
        # scene
        self._scenes = []

    @property
    def gl_context(self) -> moderngl.Context:
        return self._gl_context

    @property
    def win_size(self) -> tuple[int, int]:
        return self._WIN_SIZE
    
    @property
    def camera(self) -> Camera:
        return self._camera
    
    @property
    def time(self) -> float:
        return self._time
    
    def update_time(self, dt) -> None:
        self._time += dt
    
    def set_camera(self, camera) -> None:
        self._camera = camera
        
    def set_default_camera(self) -> None:
        self._camera.set_default_camera()

    def set_scenes(self, scenes) -> None:
        self._scenes = scenes

    def render(self, dt) -> None:
        # clear the framebuffer
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior." Big E.
        # render the scene
        for scene in self._scenes:
            scene.render()
        # swap buffers
        self._window.flip()

    def run(self) -> None:
        pyglet.app.run()
        
    def handle_keys(self, dt) -> None:
        if self._keys[pgwindow.key.Z]:
            self._camera.move("forward", dt)
        if self._keys[pgwindow.key.S]:
            self._camera.move("backward", dt)
        if self._keys[pgwindow.key.Q]:
            self._camera.move("straf_left", dt)
        if self._keys[pgwindow.key.D]:
            self._camera.move("straf_right", dt)
        if self._keys[pgwindow.key.A]:
            self._camera.move("up", dt)
        if self._keys[pgwindow.key.E]:
            self._camera.move("down", dt)
        if self._keys[pgwindow.key.RIGHT]:
            self._camera.move("right", dt)
        if self._keys[pgwindow.key.LEFT]:
            self._camera.move("left", dt)

    def on_close(self) -> None:
        for scene in self._scenes:
            scene.destroy()
