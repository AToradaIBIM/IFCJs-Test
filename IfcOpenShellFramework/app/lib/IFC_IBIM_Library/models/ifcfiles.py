"""

Clase Files que se encarga del tratado con conjuntos de archivos de tipo IFC

"""


import glob
from .ifcfile import ifcfile


class ifcfiles(list):
  #static variable
  ifcModelsLoaded = [];

  #ctor
  def __new__(cls, url_folder, guid_models):
    is_already_open = next(filter(lambda ifcmodels: ifcmodels.url == url_folder & ifcmodels.guid_files == guid_models, ifcfiles.ifcModelsLoaded), None);
    if  is_already_open != None:
      return is_already_open;
    else:
      return super(ifcfiles, cls).__new__(cls);

  # ctor-initializer
  def __init__(self,url_folder, guid_models):
    if not hasattr(self,'guid_files'):
      all_ifc_files_paths = glob.glob(f'{url_folder}/*.ifc');
      for ifc_file_path in all_ifc_files_paths:
        ifc_file_extended = ifcfile(ifc_file_path);
        self.append(ifc_file_extended);
      self.guid_files = guid_models;
      self.url = url_folder;
      ifcfiles.ifcModelsLoaded.append(self);

  # methods 
  def close_ifcs(guid_models): 
    ifcfiles.ifcModelsLoaded = list(filter(lambda ifcmodels: str(ifcmodels.guid_files) != guid_models, ifcfiles.ifcModelsLoaded))


  def get_specific_file(guid_models, file_name):
    files = next(filter(lambda ifcmodels: str(ifcmodels.guid_files) == guid_models, ifcfiles.ifcModelsLoaded), None);
    if  files != None:
      return next(filter(lambda ifcfile: ifcfile.file_name == file_name, files), None);

  
