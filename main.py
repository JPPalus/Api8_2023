from modules.core import GLEngine
from modules.shapes import *
from beta.teapot import Teapot
    

if __name__ == '__main__':
    demo = GLEngine(debug=True)
    demo.set_default_camera()
    
    # scenes = [HelloTriangle(demo)]
    # scenes = [TestCube(demo), SkeletonCube(demo)]
    scenes = [CompanionCube(demo)]
    # scenes = [Teapot(demo)]
    demo.set_scenes(scenes)

    demo.run()
