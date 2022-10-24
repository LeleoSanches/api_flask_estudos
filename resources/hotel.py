from flask_restful import Resource, reqparse
from models.hotel import HotelModel

hoteis = [
    {
        'hotel_id':'alpha',
        'nome':'Alpha Hotel',
        'estrelas':4.3,
        'diaria':420.34,
        'cidade':'Rio de Janeiro'
    },
    {
        'hotel_id':'bravo',
        'nome':'Bravo Hotel',
        'estrelas':2.3,
        'diaria':90.45,
        'cidade':'Umuarama'
    },
    {
        'hotel_id':'beta',
        'nome':'Beta Hotel',
        'estrelas':5,
        'diaria':1000.43,
        'cidade':'Londrina'
    },
]


    
class Hoteis(Resource):

    def get(self):
        return {'hoteis':[hotel.json() for hotel in HotelModel.query.all()]}

class Hotel(Resource):
    argumentos = reqparse.RequestParser()
    argumentos.add_argument('nome', type=str, required=True, help='Preencha o campo nome')
    argumentos.add_argument('estrelas', type=float, required=True, help='Preencha o campo estrelas')
    argumentos.add_argument('diaria', type=float, required=True, help='Preencha o campo diaria')
    argumentos.add_argument('cidade')


    def get(self, hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            return hotel.json()
        return {'message': 'Hotel não encontrado'}, 404

    def post(self,hotel_id):
        if HotelModel.find_hotel(hotel_id):
            return {"message":"Hotel id '{}' já existe.".format(hotel_id)}, 400

        dados = Hotel.argumentos.parse_args()
        hotel = HotelModel(hotel_id,**dados)
        try:
            hotel.save_hotel()
        except:
            return {'message':'Erro em salvar hotel'}, 500
        return hotel.json()

    def put(self,hotel_id):

        dados = Hotel.argumentos.parse_args()

        hotel_encontrado = HotelModel.find_hotel(hotel_id)
        if hotel_encontrado:
            hotel_encontrado.update_hotel(**dados)
            hotel_encontrado.save_hotel()
            return hotel_encontrado.json(), 200
        hotel = HotelModel(hotel_id,**dados)
        try:
            hotel.save_hotel()
        except:
            return {'message':'Erro em salvar hotel'}, 500
        return hotel.json(), 201

    def delete(self,hotel_id):
        hotel = HotelModel.find_hotel(hotel_id)
        if hotel:
            try:
                hotel.delete_hotel()
            except:
                return {'message':'Erro ao deletar'}, 500
            return {'message':'Hotel Deletado.'}
        return {'message': 'hotel não encontrado'}