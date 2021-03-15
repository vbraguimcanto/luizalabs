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
        return {'clients': list(map(lambda x: to_json(x), ClientModel.query.all()))}
    
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


class ProductModel(db.Model):
    __tablename__ = 'product'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    brand = db.Column(db.String, nullable=False)
    image = db.Column(db.String, nullable=False)
    review_score = db.Column(db.Numeric)
    price = db.Column(db.Numeric, nullable=False)

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def paginate_results(cls, page):
        print("Iniciando paginate")
        posts = ProductModel.query.paginate()
        print(posts.per_page)

    @classmethod
    def check_by_title(cls, title):
        return True if cls.query.filter_by(title = title).first() is not None else False
    
    @classmethod
    def check_by_id(cls, id):
        return True if cls.query.filter_by(id = id).first() is not None else False
    
    @classmethod
    def delete_by_id(cls, id):
        cls.query.filter_by(id = id).delete()
        db.session.commit()