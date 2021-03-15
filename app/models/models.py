from app import db
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

class ClientModel(db.Model):
    __tablename__ = 'client'

    email = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @classmethod
    def check_by_email(cls, email):
        return True if cls.query.filter_by(email = email).first() is not None else False
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_all(cls):
        def to_json(x):
            return {
                'email': x.email,
                'nome': x.name
            }
        return {'clientes': list(map(lambda x: to_json(x), ClientModel.query.all()))}
    
    @classmethod
    def delete_by_email(cls, email):
        cls.query.filter_by(email = email).delete()
        db.session.commit()
    
    @classmethod
    def update_by_email(cls, email, name):
        try:
            query = cls.query.filter_by(email = email).update({ClientModel.name: name})
            db.session.commit()
            return bool(query)
        
        except Exception as error:
            print("Ocorreu um erro na atualizacao de produtos. Motivo: {}".format(error))
