from flask_restful import Resource, reqparse
from models.usuario import UserModel
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash


atributos = reqparse.RequestParser()
atributos.add_argument('login', type=str, required=True, help="Campo login não pode ser deixado em branco")
atributos.add_argument('senha', type=str, required=True, help="Campo senha não pode ser deixado em branco")
  
class User(Resource):

    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'User não encontrado'}, 404

    def delete(self,user_id):
        user = UserModel.find_user(user_id)
        if user:
            user.delete_user
            return {'message':'User Deletado.'}
        return {'message': 'User não encontrado'}

class UserRegister(Resource):
    def post(self):
        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {'message':'O Login "{}" já existe'.format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message':'Usuario criado com sucesso'}, 201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and check_password_hash(user.senha, dados['senha']):
            token = create_access_token(identity=user.user_id)
            return {'acess_token': token}, 200
        return {'message':'usuario ou senha erradas'}, 401