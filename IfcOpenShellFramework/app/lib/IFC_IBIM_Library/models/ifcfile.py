
"""

Clase File que se encarga del tratado de archivos IFC

"""

import ifcopenshell
import ifcopenshell.api
import ifcopenshell.util
import ifcopenshell.util.element
import ifcopenshell.util.placement
import os
from urllib.parse import urlparse
from shapely.ops import triangulate
import shapely.geometry
from geometer import *
import numpy as np
from .geometry.face import face
import ifcopenshell.geom as geom
import ifcpatch
import ifcopenshell.template
import json


class ifcfile:
  # ctor
  def __init__(self, url):
    self.ifcfile = ifcopenshell.open(url);
    self.header = self.ifcfile.header;
    """ possibleName = self.header.file_name.name; """
    url_parsed = urlparse(url);
    self.file_name = os.path.basename(url_parsed.path);  
    self.file_name_without_extension = os.path.splitext(self.file_name)[0];
    self.dir_name = os.path.dirname(url_parsed.path);
    self.url = url;
    settings = geom.settings();
    settings.set(settings.USE_WORLD_COORDS,True);
    self.settings_geom = settings;    
    pass;



  """   def staticMethod():
    return "StaticMethod"; """
  
    
  def transform_civil_file(self):
    all_cartesian_points = self.ifcfile.by_type('IfcCartesianPoint');
    all_points = [cartesian_point.Coordinates for cartesian_point in all_cartesian_points];
    point_off_set_to_subtract = ifcfile.__calculate_min_max_point(all_points, True, 1000);

    intermediate_directory = f'{self.dir_name}\\transformated';
    if(not os.path.exists(intermediate_directory)):
      os.mkdir(intermediate_directory);

    ifcpatch.execute({
      "input": self.url,
      "output": f'{intermediate_directory}\\{self.file_name_without_extension}_toDelete.ifc',
      "recipe": "ResetAbsoluteCoordinates",
      "log": "ifcpatch.log",
      "arguments": [-point_off_set_to_subtract[0],-point_off_set_to_subtract[1],-point_off_set_to_subtract[2]],
    }) 

    intermediate_file_to_delete = ifcopenshell.open(f'{intermediate_directory}\{self.file_name_without_extension}_toDelete.ifc');
    ownerHistory = intermediate_file_to_delete.by_type('IfcOwnerHistory')[0];
    project = intermediate_file_to_delete.by_type('IfcProject')[0];
    building = intermediate_file_to_delete.by_type('IfcBuilding')[0];
    site = intermediate_file_to_delete.create_entity('IfcSite',GlobalId=ifcopenshell.guid.new(), Name='New Site', OwnerHistory = ownerHistory);
    buildingStorey = intermediate_file_to_delete.create_entity('IfcBuildingStorey',GlobalId=ifcopenshell.guid.new(), Name='New Building Storey', OwnerHistory = ownerHistory);
    offsetLocation = point_off_set_to_subtract;
    dirZ = (0.0, 0.0, 1.0);
    dirX = (1.0, 0.0, 0.0);

    local_placement_site = ifcfile.__createIfclocalplacement(intermediate_file_to_delete,offsetLocation, dirZ, dirX);
    local_placement_building_storey = ifcfile.__createIfclocalplacement(intermediate_file_to_delete,(0.0,0.0,0.0), dirZ, dirX);

    building.ObjectPlacement.PlacementRelTo = local_placement_site;
    local_placement_building_storey.PlacementRelTo = building.ObjectPlacement;

    buildingStorey.ObjectPlacement = local_placement_building_storey;
    site.ObjectPlacement = local_placement_site;

    for prod in building.ContainsElements[0].RelatedElements:
      ifcopenshell.api.run("spatial.assign_container", intermediate_file_to_delete, product=prod, relating_structure=buildingStorey);

    ifcopenshell.api.run("aggregate.assign_object", intermediate_file_to_delete, product=site, relating_object=project);
    ifcopenshell.api.run("aggregate.assign_object", intermediate_file_to_delete, product=building, relating_object=site);
    ifcopenshell.api.run("aggregate.assign_object", intermediate_file_to_delete, product=buildingStorey, relating_object=building);

    intermediate_file_to_delete.write(f'{self.dir_name}\\transformated\\{self.file_name}');
    os.remove(f'{intermediate_file_to_delete}\{self.file_name_without_extension}_toDelete.ifc');
