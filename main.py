from modules.core import GLEngine
from modules.shapes import TestCube
# from modules.teapot import Teapot
    

if __name__ == '__main__':
    demo = GLEngine()
    demo.set_default_camera()
    
    scene = TestCube(demo)
    demo.set_scene(scene)

    demo.run()
