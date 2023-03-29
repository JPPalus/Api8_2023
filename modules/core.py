import platform
import pyglet as pg
import pyglet.app as pgapp
import pyglet.window as pgwindow
import pyglet.clock as pgclock
import moderngl
from modules.camera import Camera
from modules.light import Light
from collections.abc import Generator


if platform.system() == "Darwin":
    pg.options["shadow_window"] = False
pg.options["debug_gl"] = False

class GLEngine:
    def __init__(self, win_size=(1280, 720), fps=60, debug = False, allow_mouse_controls = False) -> None:
        self._debug = debug
        self._allow_mouse_controls = allow_mouse_controls
        # init pyglet and OpenGL context
        self._WIN_SIZE = win_size
        self._window = pgwindow.Window(vsync=False)
        self._window_context = self._window.context
        # keeps track of time
        self._time = 0
        # keyboard event handler
        self._keys_state = {pgwindow.key : bool}
        self._window.push_handlers(on_mouse_motion = self.on_mouse_motion,
                                   on_key_press = self.on_key_press,
                                   on_key_release = self.on_key_release)
        # detect and use existing OpenGL context
        self._gl_context = moderngl.create_context()
        # self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.CULL_FACE | moderngl.PROGRAM_POINT_SIZE)
        self.gl_context.enable_only(moderngl.DEPTH_TEST | moderngl.PROGRAM_POINT_SIZE)
        # mouse settings
        self._window.set_exclusive_mouse(True)
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior."
        # loop handler
        pgclock.schedule(self.update_time)
        pgclock.schedule(self.handle_key_pressed)
        pgclock.schedule_interval(self.render, 1 / fps)
        # camera
        self._camera = Camera(self)
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
    
    @property
    def debug(self) -> bool:
        return self._debug
    
    @property # -> Generator['TODO, custom class']
    def scenes(self):
        for scene in self._scenes:
            yield scene
            
    @property # -> Generator['TODO, custom class']
    def light(self):
        return self._light
        
    def update_time(self, dt) -> None:
        self._time += dt
    
    def set_camera(self, camera) -> None:
        self._camera = camera
        
    def set_default_camera(self) -> None:
        self._camera.set_default_camera()

    def set_scenes(self, scenes) -> None:
        self._scenes = scenes
        
    def set_lights(self, lights) -> None:
        self._light = lights

    def render(self, dt) -> None:
        # clear the framebuffer
        self._gl_context.clear(color=(0.9, 0.8, 0.01)) # "The fact that gold exists makes every other colours equally inferior." Big E.
        # render the scene
        for scene in self._scenes:
            scene.render()
        # swap buffers
        self._window.flip()

    def run(self) -> None:
        pgapp.run()
        
    def handle_key_pressed(self, dt) -> None:
        if self._keys_state.get(pgwindow.key.Z):
            self._camera.move("forward", dt)
        if self._keys_state.get(pgwindow.key.S):
            self._camera.move("backward", dt)
        if self._keys_state.get(pgwindow.key.Q):
            self._camera.move("straf_left", dt)
        if self._keys_state.get(pgwindow.key.D):
            self._camera.move("straf_right", dt)
        if self._keys_state.get(pgwindow.key.A):
            self._camera.move("straf_up", dt)
        if self._keys_state.get(pgwindow.key.E):
            self._camera.move("straf_down", dt)
        if self._keys_state.get(pgwindow.key.RIGHT):
            self._camera.move("right", dt)
        if self._keys_state.get(pgwindow.key.LEFT):
            self._camera.move("left", dt)
        if self._keys_state.get(pgwindow.key.UP):
            self._camera.move("up", dt)
        if self._keys_state.get(pgwindow.key.DOWN):
            self._camera.move("down", dt)

    def on_key_press(self, symbol, modifier) -> None:
        # options 
        # j : activate / deactivate debug mode
        if symbol == pgwindow.key.J:
            self._debug = not self._debug
            debug_state = 'activated' if self._debug else 'deactivated'
            print(f'debug mode {debug_state}')   
        # r : reset camera and models to default position
        if symbol == pgwindow.key.R:
            self._camera.reset_camera()
            if self._debug:
                print(f'camera reset to {self._camera._default_position}')
        # l : look at the scene being rendered
        if symbol == pgwindow.key.L:
            self._camera.look_at_scene()
        # m : allow / disable mouse camera controls
        if symbol == pgwindow.key.M:
            self._allow_mouse_controls = not self._allow_mouse_controls
            if self._debug:
                mouse_controls_state = 'activated' if self._allow_mouse_controls else 'deactivated'
                print(f'camera controls with mouse {mouse_controls_state}')
        # move controls
        if symbol == pgwindow.key.Z:
            self._keys_state[pgwindow.key.Z] = True
        if symbol == pgwindow.key.S:
            self._keys_state[pgwindow.key.S] = True
        if symbol == pgwindow.key.Q:
            self._keys_state[pgwindow.key.Q] = True
        if symbol == pgwindow.key.D:
            self._keys_state[pgwindow.key.D] = True
        if symbol == pgwindow.key.A:
            self._keys_state[pgwindow.key.A] = True
        if symbol == pgwindow.key.E:
            self._keys_state[pgwindow.key.E] = True
        if symbol == pgwindow.key.RIGHT:
            self._keys_state[pgwindow.key.RIGHT] = True
        if symbol == pgwindow.key.LEFT:
            self._keys_state[pgwindow.key.LEFT] = True
        if symbol == pgwindow.key.UP:
            self._keys_state[pgwindow.key.UP] = True
        if symbol == pgwindow.key.DOWN:
            self._keys_state[pgwindow.key.DOWN] = True
            
    def on_key_release(self, symbol, modifier) -> None:
        # move controls
        if symbol == pgwindow.key.Z:
            self._keys_state[pgwindow.key.Z] = False
        if symbol == pgwindow.key.S:
            self._keys_state[pgwindow.key.S] = False
        if symbol == pgwindow.key.Q:
            self._keys_state[pgwindow.key.Q] = False
        if symbol == pgwindow.key.D:
            self._keys_state[pgwindow.key.D] = False
        if symbol == pgwindow.key.A:
            self._keys_state[pgwindow.key.A] = False
        if symbol == pgwindow.key.E:
            self._keys_state[pgwindow.key.E] = False
        if symbol == pgwindow.key.RIGHT:
            self._keys_state[pgwindow.key.RIGHT] = False
        if symbol == pgwindow.key.LEFT:
            self._keys_state[pgwindow.key.LEFT] = False
        if symbol == pgwindow.key.UP:
            self._keys_state[pgwindow.key.UP] = False
        if symbol == pgwindow.key.DOWN:
            self._keys_state[pgwindow.key.DOWN] = False
            
    def on_mouse_motion(self, x, y, dx, dy) -> None:
        if self._allow_mouse_controls == True :
            self._camera.rotate(x, y, dx, dy)

    def on_close(self) -> None:
        for scene in self._scenes:
            scene.destroy()
