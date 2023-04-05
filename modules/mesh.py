import numpy as np



class Mesh:
    def __init__(self, engine) -> None:
        self._engine = engine
    
    def get_vertex_data(self) -> np.ndarray:
        ...
        
    @staticmethod
    def get_vertices_from_surface(vertices, surfaces) -> np.ndarray:
        data = [vertices[indice]
                for triangle in surfaces 
                    for indice in triangle]
        return np.array(data, dtype='f4')
        

class TexturedCubeMesh(Mesh):
    def __init__(self, engine) -> None:
        super().__init__(engine)
    
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
        
        tex_coord = ((0, 1), (1, 1), (1, 0), (0, 0))
        
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
    
    
class SolidCubeMesh(Mesh):
    def __init__(self, engine) -> None:
        super().__init__(engine)
    
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
    

class WireCubeMesh(Mesh):
    def __init__(self, engine) -> None:
        super().__init__(engine)
        
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

