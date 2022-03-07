"""

Código que crea el BluePrint con los EndPoints que se encargan de los datos geométricos

"""

#Imports

#Importamos FLask
from flask import Blueprint, make_response


#Creamos el BluePrint
endpoints_test = Blueprint('test', __name__)

#EndPoint de prueba que devuelve Hello World (GET)
@endpoints_test.route('/helloworld', methods=['GET'])
def hello_world():
  return make_response("hello World", 200);