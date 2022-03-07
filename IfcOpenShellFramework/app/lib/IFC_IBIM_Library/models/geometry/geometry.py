
"""

Clase geometry que se encarga del tratado de geometría básica

"""

from ..ifcfiles import ifcfiles
import json
from ifcopenshell import geom
import shapely
from geometer import *
import numpy as np
from .face import face
import math

class geometry:
  
  STEEL_DENSITY = 7850
  ALUMINUM_DENSITY = 2700
  CONCRETE_DENSITY = 2200
  REINFORCED_CONCRETE_DENSITY = 2500
  WOOD_DENSITY = 600
  # methods
  def get_geom_of_specific_ifcelement(self, instance):
    settings = geom.settings();
    settings.set(settings.USE_WORLD_COORDS,True);
    settings_geom = settings;    
    if(instance.Representation != None):
      shape = geom.create_shape(settings_geom, instance)
      
      ios_vertices = shape.geometry.verts
      ios_edges = shape.geometry.edges
      ios_faces = shape.geometry.faces

      vertices = [
          ios_vertices[i : i + 3] for i in range(0, len(ios_vertices), 3)
      ]
      
      edges = [ios_edges[i : i + 2] for i in range(0, len(ios_edges), 2)]
      faces = [tuple(ios_faces[i : i + 3]) for i in range(0, len(ios_faces), 3)]
      bbox = self.get_bounding_box_of_ifcelement(vertices);
      print(bbox)
      return {
        "Vertices": vertices,
        "Edges": edges,
        "Faces": faces,
        "BoundingBox": bbox,
        "GlobalId": instance.GlobalId,
        "EntityLabel": instance.id()
      }
  
  def get_boundary_points_for_specific_instance(self, instance, file_name):
    geom_of_instance = self.get_geom_of_specific_ifcelement(instance);
    if(geom_of_instance != None):
      p = shapely.geometry.Polygon(geom_of_instance['Vertices']);

      geom = p.convex_hull;
      a, b = geom.exterior.coords.xy;
      points_tuple = tuple(list(zip(a,b)));

      return {
        "FileName": file_name,
        "GlobalId": instance.GlobalId,
        "Points": points_tuple
        };

  def get_all_faces(self, instance):
    geom_of_instance = self.get_geom_of_specific_ifcelement(instance);
    if(geom_of_instance != None):
      faces = [];
      for face_geom in geom_of_instance['Faces']:
        try:
          point_one_str = geom_of_instance['Vertices'][face_geom[0]];
          point_two_str = geom_of_instance['Vertices'][face_geom[1]];
          point_three_str = geom_of_instance['Vertices'][face_geom[2]];
          point_one = Point(point_one_str[0],point_one_str[1],point_one_str[2]);
          point_two = Point(point_two_str[0],point_two_str[1],point_two_str[2]);
          point_three = Point(point_three_str[0],point_three_str[1],point_three_str[2]);
          points = [point_one, point_two, point_three];
          plane = Plane(point_one, point_two, point_three);
          
          new_tensor = plane.T.array;
          flag = False;
          for face_added in faces:
            if(np.allclose(face_added.tensor, new_tensor)):
              face_added.add_vertices(points);
              flag = True;
              break;

          if(not flag):
            faces.append(face(new_tensor,points));
        except:
          pass;
      
      return json.dumps([face.to_json() for face in faces]);


  def get_volume_of_an_especific_ifcelement(self, instance):
    geom_of_instance = self.get_geom_of_specific_ifcelement(instance);
    if(geom_of_instance != None):
      vols = 0;
      for face_geom in geom_of_instance['Faces']:
        point_one = geom_of_instance['Vertices'][face_geom[0]];
        point_two = geom_of_instance['Vertices'][face_geom[1]];
        point_three = geom_of_instance['Vertices'][face_geom[2]];
        
        vols += self.signed_volume_of_triangle(point_one, point_two, point_three)
      return abs(vols)

            
  def signed_volume_of_triangle(self, v1, v2, v3):
    v321 = v3[0] * v2[1] * v1[2];
    v231 = v2[0] * v3[1] * v1[2];
    v312 = v3[0] * v1[1] * v2[2];
    v132 = v1[0] * v3[1] * v2[2];
    v213 = v2[0] * v1[1] * v3[2];
    v123 = v1[0] * v2[1] * v3[2];
    
    return  (1.0/6.0)*( - v321 + v231 + v312 - v132 - v213 + v123 )


  def calculate_surface_of_an_ifcelement(self, instance):
    all_faces =json.loads(self.get_all_faces(instance))
    surface = 0
    for total_area_face in all_faces:
      surface += total_area_face["TotalArea"]
    return surface

  def calculate_weight_of_an_ifcelement(self, instance, material):
    volume = self.get_volume_of_an_especific_ifcelement(instance)
    if(material == "Steel"):
      mass = volume * self.STEEL_DENSITY
    elif(material == "Aluminum"):
      mass = volume * self.ALUMINUM_DENSITY
    elif(material == "Concrete"):
      mass = volume * self.CONCRETE_DENSITY
    elif(material == "Reinforced Concrete"):
      mass = volume * self.REINFORCED_CONCRETE_DENSITY
    elif(material == "Wood"):
      mass = volume * self.WOOD_DENSITY
    return mass



#En desarrollo
  def __create_ifc_axis2placement(self, f, point, dir1, dir2):
    point = f.createIfcCartesianPoint(point)
    dir1 = f.createIfcDirection(dir1)
    dir2 = f.createIfcDirection(dir2)
    axis2placement = f.createIfcAxis2Placement3D(point, dir1, dir2)
    return axis2placement

  # Creates an IfcLocalPlacement from Location, Axis and RefDirection, specified as Python tuples, and relative placement
  def __create_ifc_local_placement(self, f, point, dir1, dir2, relative_to=None):
      axis2placement = self.__create_ifc_axis2placement(f, point, dir1, dir2)
      ifc_local_placement2 = self.__create_ifc_local_placement(relative_to, axis2placement)
      return ifc_local_placement2
  
  def __calculate_min_max_point(self, allPoints, flagMinValue, offset = 0):
    x_coordinates = [point[0] for point in allPoints if(point[0] > offset)];
    possible_min_x = min(x_coordinates) if len(x_coordinates) > 0 else 0.0;
    possible_max_x = max(x_coordinates) if len(x_coordinates) > 0 else 0.0;
    min_x = possible_min_x if possible_min_x != None else 0.0;
    max_x = possible_max_x if possible_max_x != None else 0.0;

    y_coordinates = [point[1] for point in allPoints if(point[1] > offset)]
    possible_min_y = min(y_coordinates) if len(y_coordinates) > 0 else 0.0;
    possible_max_y = max(y_coordinates) if len(y_coordinates) > 0 else 0.0;
    min_y = possible_min_y if possible_min_y != None else 0.0;
    max_y = possible_max_y if possible_max_y != None else 0.0;

    z_coordinates = [point[2] for point in allPoints if(point[2] > offset)];
    possible_min_z = min(z_coordinates) if len(z_coordinates) > 0 else 0.0;
    possible_max_z = max(z_coordinates) if len(z_coordinates) > 0 else 0.0;
    min_z = possible_min_z if possible_min_z != None else 0.0;
    max_z = possible_max_z if possible_max_z != None else 0.0;

    return (min_x, min_y, min_z) if flagMinValue else (max_x, max_y, max_z);

  def get_bounding_box_of_ifcelement(self, vertices):
    min_point = self.__calculate_min_max_point(vertices,True);
    max_point = self.__calculate_min_max_point(vertices,False);
    return [min_point, max_point];