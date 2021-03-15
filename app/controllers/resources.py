import json
from flask import jsonify
from flask import request
from flask_restful import Resource, reqparse
from flask_expects_json import expects_json
from jsonschema import validate
from app.models.models import ClientModel, ProductModel, ClientProductModel

schema_client = {
    'type': 'object',
    'properties': {
        'name': {'type': 'string'},
        'email': {'type': 'string'}
    },
    'required': ['name', 'email']
}

schema_product = {
    'type': 'object',
    'properties': {
        'title': {'type': 'string'},
        'brand': {'type': 'string'},
        'image': {'type': 'string'},
        'price': {'type': 'number'},
        'reviewScore': {'type': 'number'}
    },
    'required': ['title', 'brand', 'image', 'price', 'reviewScore']
}

schema_product_list = {
    'type': 'object',
    'properties': {
        'product_id': {'type': 'integer'},
        'email': {'type': 'string'},
    },
    'required': ['product_id', 'email']
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
                    "message": "Cliente ja cadastrado"
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

    @expects_json(schema_product)
    def post(self):
        try:
            self.payload_request = json.loads(request.get_data())

            if not ProductModel.check_by_title(self.payload_request['title']):
                product = ProductModel(
                    title = self.payload_request['title'],
                    brand = self.payload_request['brand'],
                    image = self.payload_request['image'], 
                    price = self.payload_request['price'],
                    review_score = self.payload_request['reviewScore']         
                )
                product.save()
            else:
                return {
                    "message": "Produto ja cadastrado"
                }, 200

            return {
                "message": "Produto cadastrado com sucesso"
            }, 201


        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500

    # tratar para paginas enviadas menores que zero
    def get(self):
        try:
            self.logger.info("Recebendo request para buscar produtos")
            page = request.args.get('page', 1, type=int)
            def to_json(x):
                return {
                    'id': x.id,
                    'title': x.title,
                    'brand': x.brand,
                    'price': float("{:.2f}".format(x.price)),
                    'image': x.image,
                    'reviewScore': float("{:.2f}".format(x.review_score))
                }
            return {'products': list(map(lambda x: to_json(x), ProductModel.query.paginate(page=page, per_page=15, error_out=False).items))}
        
        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500
    
    def delete(self):
        try:
            self.logger.info("Recebendo request para deletar produtos")
            product_id = request.args.get('id')
            if ProductModel.check_by_id(product_id):
                ProductModel.delete_by_id(product_id)
                return {
                    "message": "Produto deletado"
                }, 200
            else:
                return {
                    "message": "Produto nao encontrado"
                }, 200

            
        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500

class ClientProduct(Resource):
    
    def __init__(self, **kwargs):
        self.logger = kwargs.get('logging')

    @expects_json(schema_product_list)
    def post(self):
        try:
            self.payload_request = json.loads(request.get_data())

            if not ClientProductModel.check_product_by_email(self.payload_request['product_id'], self.payload_request['email']):
                if ClientModel.check_by_email(self.payload_request['email']) and ProductModel.check_by_id(self.payload_request['product_id']):
                    client_product = ClientProductModel(
                        product_id = self.payload_request['product_id'],
                        client_id = self.payload_request['email']
                    )
                    client_product.save()

                else:
                    return {
                        "message": "email e/ou product_id nao existem"
                    }, 200

            else:
                return {
                    "message": "Produto ja cadastrado na lista"
                }, 200

            return {
                "message": "Produto cadastrado na lista com sucesso"
            }, 201


        except Exception as error:
            self.logger.error(f"Erro ao receber a requisicao. Motivo: {error}")
            return "", 500
