import json
from flask import jsonify
from flask import request
from flask_restful import Resource, reqparse
from flask_expects_json import expects_json
from jsonschema import validate
from app.models.models import ClientModel

schema_client = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'}
    },
    'required': ['name', 'email']
}

class Client(Resource):
    
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logging')

    @expects_json(schema_client)
    def post(self):
        try:
            self.logger.info("Recebendo request para registrar cliente")
            self.payload_request = json.loads(request.get_data())

            if not ClientModel.check_by_email(self.payload_request['email']):
                client = ClientModel(
                    email = self.payload_request['email'],
                    name = self.payload_request['name']                
                )
                client.save()
            else:
                return {
                    "message": "Cliente já cadastrado"
                }, 200

            return {
                "message": "Cliente cadastrado com sucesso"
            }, 201


        except ValueError as error:
            return "", 400

        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500

    # adicionar filtro de visualização e paginação
    def get(self):
        try:
            self.logger.info("Recebendo request para buscar clientes")
            clients_json = ClientModel.find_all()
            return clients_json, 200
            
        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500
    
    def delete(self):
        try:
            self.logger.info("Recebendo request para deletar clientes")
            email = request.args.get('email')
            if ClientModel.check_by_email(email):
                ClientModel.delete_by_email(email)
                return {
                    "message": "Cliente deletado"
                }, 200
            else:
                return {
                    "message": "Cliente nao encontrado"
                }, 200

            
        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500
    
    
    @expects_json(schema_client)
    def put(self):
        try:
            self.logger.info("Recebendo request para atualizar cliente")
            self.payload_request = json.loads(request.get_data())

            if ClientModel.check_by_email(self.payload_request['email']):
                ClientModel.update_by_email(self.payload_request['email'], self.payload_request['name'])
            else:
                return {
                    "message": "Cliente nao encontrado"
                }, 200

            return {
                "message": "Cliente atualizado com sucesso"
            }, 200

        except ValueError as error:
            return "", 400

        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500


class Product(Resource):
    
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logging')

    # criar schema json
    def post(self):
        pass

    # tratar para paginas enviadas menores que zero
    def get(self):
        pass

    # realizar a exclusao via ID
    def delete(self):
        pass

    def put(self):
        pass

class ClientProduct(Resource):
    
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logging')

    # criar schema json
    def post(self):
        pass

    # tratar para paginas enviadas menores que zero
    def get(self):
        pass

    # realizar a exclusao via ID do produto e e-mail
    def delete(self):
        pass

    def put(self):
        pass