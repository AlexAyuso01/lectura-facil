import unittest
from unittest.mock import patch
import pandas as pd
from io import BytesIO

from app import app as flask_app

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()

    # El decorador @patch se utiliza para modificar el comportamiento de las funciones
    # en el contexto del test. Aquí estamos modificando el comportamiento de
    # SentenceTransformer, pytorch_cos_sim y read_csv
    @patch('app.SentenceTransformer')
    @patch('app.util.pytorch_cos_sim')
    @patch('app.pd.read_csv')
    def test_get_similarity(self, mock_read_csv, mock_pytorch_cos_sim, mock_sentence_transformer):
        # Aquí estamos diciendo que cuando se llame a pytorch_cos_sim().item() queremos que devuelva 0.9
        mock_pytorch_cos_sim.return_value.item.return_value = 0.9

        # Aquí estamos diciendo que cuando se llame a SentenceTransformer().encode() queremos que devuelva [1, 2, 3, 4, 5]
        mock_sentence_transformer.return_value.encode.return_value = [1, 2, 3, 4, 5]

        # Aquí estamos diciendo que cuando se llame a pd.read_csv() queremos que devuelva un DataFrame específico
        mock_read_csv.return_value = pd.DataFrame({
            'frase_original': ['Hola ¿Cómo estás?'],
            'frase_adaptada': ['Hola ¿Qué tal?'],
            'semanticamente_similares': ['SI']
        })

        # Creamos un archivo CSV falso
        data_csv = """
        frase_original;frase_adaptada;semanticamente_similares
        Hola ¿Cómo estás?;Hola ¿Qué tal?;SI
        """

        mock_csv = (BytesIO(data_csv.encode()), "mock.csv")
        # Llamamos al endpoint '/similarity' con el archivo CSV falso
        response = self.app.post(
            '/similarity',
            content_type='multipart/form-data',
            data={
                'file': mock_csv
            }
        )

        # Comprobamos que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Comprobamos que los datos de la respuesta son correctos
        expected_data = [
            {
                'frase_original': 'Hola ¿Cómo estás?',
                'frase_adaptada': 'Hola ¿Qué tal?',
                'similitudes': [0.9, 0.9, 0.9],
                'predicciones': [1, 1, 1],
                'etiqueta_real': 1
            }
        ]
        self.assertEqual(response.get_json(), expected_data)

        # Test para el caso en el que no se proporciona un archivo
    def test_get_similarity_no_file(self):
        # Llamamos al endpoint '/similarity' sin proporcionar un archivo
        response = self.app.post('/similarity', content_type='multipart/form-data')

        # Comprobamos que el código de estado de la respuesta es 400 (Bad Request)
        self.assertEqual(response.status_code, 400)
        # Comprobamos que el cuerpo de la respuesta es el esperado
        self.assertEqual(response.get_data(as_text=True), "No file found")

        # Test para el caso en el que el archivo CSV no es válido
    def test_get_similarity_invalid_csv(self):
        # Creamos un archivo CSV inválido
        data_csv = """
        this is not a valid CSV file
        """

        mock_csv = (BytesIO(data_csv.encode()), "mock.csv")
        # Llamamos al endpoint '/similarity' con el archivo CSV inválido
        response = self.app.post(
            '/similarity',
            content_type='multipart/form-data',
            data={
                'file': mock_csv
            }
        )

        # Comprobamos que el código de estado de la respuesta es 400 (Bad Request)
        self.assertEqual(response.status_code, 400)

if __name__ == '__main__':
    unittest.main()
