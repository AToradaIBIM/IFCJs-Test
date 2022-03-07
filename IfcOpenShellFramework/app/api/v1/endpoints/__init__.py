"""

Init que establece a un BluePrint principal otros BluePrints con rutas específicas

"""

#Imports

#Import de Flask
from flask import Blueprint

#Imports de los otros BluePrints
from .converter import endpoints_converter
from .files import endpoints_files
from .geometry import endpoints_geometry
from .test import endpoints_test

#Creamos un BluePrint principal
ifcOpenShellFramework = Blueprint('ifcopenshell', __name__, url_prefix="/ifcopenshell/v1")

#Al BluePrint principal se le añaden los BluePrints creados para cada tipo de consulta

#EndPoints de los Conversores
ifcOpenShellFramework.register_blueprint(endpoints_converter,  url_prefix='/converter')
#EndPoints de los Archivos
ifcOpenShellFramework.register_blueprint(endpoints_files,  url_prefix='/files')
#EndPoints de la Geometría
ifcOpenShellFramework.register_blueprint(endpoints_geometry,  url_prefix='/geometry')
#EndPoints de tipo Test
ifcOpenShellFramework.register_blueprint(endpoints_test,  url_prefix='/test')

