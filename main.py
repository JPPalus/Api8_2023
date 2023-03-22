from modules.core import GLEngine
from modules.shapes import HelloTriangle

    

if __name__ == '__main__':
    demo = GLEngine()
    context = demo.get_gl_context()
    scene = HelloTriangle(context)
    demo.set_scene(scene)
    demo.run()
