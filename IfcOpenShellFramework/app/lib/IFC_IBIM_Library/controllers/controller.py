"""

Clase general que se encarga de proporcionar acceso a los diferentes métodos de la librería

"""

from ..models.ifcfiles import ifcfiles
from ..models.geometry.geometry import geometry
import json
import ifcopenshell

class controller():
  
  def __init__(self):
    self.geom = geometry()


  def open(self, data_request): 
    return ifcfiles(data_request["pathOfFiles"], data_request["guidModels"]).guid_files

  def close(self, guid_models): 
    ifcfiles.close_ifcs(guid_models)

  def transform_civil_ifc(self, guid_models, body_json):
    model_names = body_json['models']
    for model_name in model_names:
      file_search = ifcfiles.get_specific_file(guid_models, model_name)
      if(file_search != None):
        file_search.transform_civil_file();          
    return 'Archivos procesados correctamente'
  
  def get_boundary_geom_instance(self,guid_models, body_json):
    results = [];
    for model in body_json:
      file_name = model['model']
      guids = model['guids']

      file_search = ifcfiles.get_specific_file(guid_models, file_name)
      if(file_search != None):
        for guid in guids: 
          results.append(self.geom.get_boundary_points_for_specific_instance(file_search.ifcfile.by_guid(guid), file_search.file_name))
    return json.dumps(results)

  def get_basic_geom_instance(self,guid_models, body_json):
    results = []
    file_name = body_json['model']
    guids = body_json['guids']

    file_search = ifcfiles.get_specific_file(guid_models, file_name)
    if(file_search != None):
      for guid in guids: 
        results.append(self.geom.get_geom_of_specific_ifcelement(file_search.ifcfile.by_guid(guid)))
    return json.dumps(results)
  
  def get_all_faces(self,guid_models, body_json):
    results = [];
    for model in body_json:
      file_name = model['model']
      guids = model['guids']

      file_search = ifcfiles.get_specific_file(guid_models, file_name)
      if(file_search != None):
        for guid in guids:
          results.append(self.geom.get_all_faces(file_search.ifcfile.by_guid(guid)))
    return json.dumps(results)

  def get_volume_of_an_especific_ifcelement(self, guid_models, body_json):
    file_name = body_json['model']
    guid = body_json['guid']

    file_search = ifcfiles.get_specific_file(guid_models, file_name)
    
    if(file_search != None):
      return self.geom.get_volume_of_an_especific_ifcelement(file_search.ifcfile.by_guid(guid))
    
  def get_surface_of_an_especific_ifcelement(self, guid_models, body_json):
    file_name = body_json['model']
    guid = body_json['guid']

    file_search = ifcfiles.get_specific_file(guid_models, file_name)
    
    if(file_search != None):
      return self.geom.calculate_surface_of_an_ifcelement(file_search.ifcfile.by_guid(guid))

  def get_weight_of_an_especific_ifcelement(self, guid_models, body_json):
    file_name = body_json['model']
    guid = body_json['guid']
    material = body_json['material']
    identifier = body_json['id']
    print(identifier)
    file_search = ifcfiles.get_specific_file(guid_models, file_name)
    print(type(file_search.ifcfile.by_id(identifier)))
    if(file_search != None):
      return self.geom.calculate_weight_of_an_ifcelement(file_search.ifcfile.by_id(identifier), material)