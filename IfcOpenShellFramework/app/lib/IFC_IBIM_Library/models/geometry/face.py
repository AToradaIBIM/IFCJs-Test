
"""

Clase Face que se encarga del cálculo de datos de las caras

"""

from geometer import *

class face:
  # ctor-initializer
  def __init__(self, tensor, vertices):
    self.tensor = tensor;
    self.vertices = vertices;
  
  @property
  def polygons(self):
    if(not hasattr(self,'_polygons')):
      self._polygons = [];
      for i in range(0,len(self.vertices),3):
        new_polygon = Polygon(self.vertices[i], self.vertices[i+1], self.vertices[i+2]);
        self._polygons.append(new_polygon);
    return self._polygons;

  @property
  def total_area(self):
    if(not hasattr(self,'_totalArea')):
      self._total_area = 0.0;
      for poly in self.polygons:
        self._total_area += poly.area;
    return self._total_area;

  def add_vertices(self, new_vertices):
    for vert in new_vertices:
      """if(not vert in self.vertices): """
      self.vertices.append(vert);
  
  def to_json(self):
    return {
      "TotalArea" : self.total_area,
      "Tensor": str(self.tensor)
    }
    """     return json.dumps(self, default= lambda thisObj: thisObj.__dict__) """