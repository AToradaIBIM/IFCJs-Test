"""

Código que crea el BluePrint con los EndPoints que se encargan de los datos geométricos

"""

#Imports

#Importamos FLask

from flask import Blueprint, request, make_response, jsonify
#Import de la instancia estática de la librería
from app.api.v1.controller import controller

#Creamos el BluePrint
endpoints_geometry = Blueprint('geometry', __name__)

#EndPoint del Perímetro geométrico del modelo pasado (POST)
@endpoints_geometry.route('/boundarygeominstance/<guidmodels>', methods=['POST'])
def boundary_geom_instance(guidmodels):
  data = request.get_json();  
  results = controller.get_boundary_geom_instance(guidmodels,data);
  return make_response(str(results),200);

#EndPoint de la geometría básica del modelo pasado (POST)
@endpoints_geometry.route('/basicgeominstance/<guidmodels>', methods=['POST'])
def basic_geom_instance(guidmodels):
  data = request.get_json();  
  results = controller.get_basic_geom_instance(guidmodels,data);
  return make_response(str(results),200);

#EndPoint de las caras del modelo pasado (POST)
@endpoints_geometry.route('/allfaces/<guidmodels>', methods=['POST'])
def get_all_faces(guidmodels):
  data = request.get_json();  
  results = controller.get_all_faces(guidmodels,data);
  return make_response(str(results),200);

@endpoints_geometry.route('/volumeinstance/<guidmodels>', methods=['POST'])
def get_volume_instance(guidmodels):
  data = request.get_json();
  results = controller.get_volume_of_an_especific_ifcelement(guidmodels,data);
  return make_response(str(results),200);

@endpoints_geometry.route('/surfaceinstance/<guidmodels>', methods=['POST'])
def get_surface_instance(guidmodels):
  data = request.get_json();
  results = controller.get_surface_of_an_especific_ifcelement(guidmodels,data);
  return make_response(str(results),200);

@endpoints_geometry.route('/weightinstance/<guidmodels>', methods=['POST', 'OPTIONS'])
def get_weight_instance(guidmodels):
  if request.method == "OPTIONS": # CORS preflight
      return _build_cors_preflight_response()
      pass
  elif request.method == "POST": # The actual request following the preflight
      data = request.get_json()
      results = controller.get_weight_of_an_especific_ifcelement(guidmodels,data);
      return _corsify_actual_response(jsonify(results))

  return make_response(str(results),200);

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response