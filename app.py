from flask import *
from flask_cors import CORS, cross_origin
from flask_restful import Resource, Api, reqparse
from json import dumps
import werkzeug
from models.Excel import Excel


app = Flask(__name__)
api = Api(app)
CORS(app)

class ExcelTool(Resource):
    
    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument('file', type=werkzeug.datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file_excel = args['file']
        date_query = request.form.get('date_query')
        excel = Excel(file_excel, date_query)
        
        return make_response(jsonify(excel.result()), 200)
    

api.add_resource(ExcelTool, '/') # Route_1

if __name__ == '__main__':
    app.run(debug=True)