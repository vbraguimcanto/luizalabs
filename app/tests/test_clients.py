import unittest
from flask import json
from app.controllers.resources import Client, ClientProduct, Product

class InputTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.maxDiff = None

    """
        Caso de Teste: CNPJ invalido
        URL: /api/v1/transacao/estabelecimento
    """
    def test_input_transaction_get_invalid_cnpj(self):
        response = self.app.get('/api/v1/transacao/estabelecimento?cnpj=1', content_type='application/json')
        self.assertEqual(response.status_code, 400)
    

    
if __name__ == '__main__':
    unittest.main()