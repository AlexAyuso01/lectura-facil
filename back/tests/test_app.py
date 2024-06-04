import unittest
from unittest.mock import patch
import pandas as pd
from io import BytesIO
import sys
import os

# Asegúrate de que el directorio `back` esté en sys.path para importar `app` correctamente
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app as flask_app, evaluate_quality, evaluate_individual_quality

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
        # Llamamos al endpoint '/upload' con el archivo CSV falso
        response = self.app.post(
            '/upload',
            content_type='multipart/form-data',
            data={
                'file': mock_csv
            }
        )

        # Comprobamos que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)
        # Comprobamos que los datos de la respuesta son correctos
        response_data = response.get_json()
        self.assertIn('original', response_data[0])
        self.assertIn('adapted', response_data[0])
        self.assertIn('metrics', response_data[0])
        self.assertIn('overall_quality', response_data[0])
        self.assertIn('individual_qualities', response_data[0])

    # Test para el caso en el que no se proporciona un archivo
    def test_upload_file_no_file_part(self):
        response = self.app.post('/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "No file part")

    @patch('app.pd.read_csv')
    def test_upload_file_invalid_csv(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing CSV")

        data_csv = "this is not a valid CSV file"
        mock_csv = (BytesIO(data_csv.encode()), "mock.csv")

        response = self.app.post(
            '/upload',
            content_type='multipart/form-data',
            data={'file': mock_csv}
        )

        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Error parsing CSV")

class AdditionalTests(unittest.TestCase):
    def setUp(self):
        self.app = flask_app.test_client()

    @patch('app.pd.read_csv')
    def test_upload_file_success(self, mock_read_csv):
        # Mock del DataFrame
        mock_read_csv.return_value = pd.DataFrame({
            'frase_original': ['Hola ¿Cómo estás?'],
            'frase_adaptada': ['Hola ¿Qué tal?']
        })

        # Creación del archivo CSV falso
        data_csv = """
        frase_original;frase_adaptada
        Hola ¿Cómo estás?;Hola ¿Qué tal?
        """
        mock_csv = (BytesIO(data_csv.encode()), "mock.csv")

        # Llamada al endpoint '/upload' con el archivo CSV falso
        response = self.app.post(
            '/upload',
            content_type='multipart/form-data',
            data={'file': mock_csv}
        )

        # Comprobamos que el código de estado de la respuesta es 200 (OK)
        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertIn('original', response_data[0])
        self.assertIn('adapted', response_data[0])
        self.assertIn('metrics', response_data[0])
        self.assertIn('overall_quality', response_data[0])
        self.assertIn('individual_qualities', response_data[0])

    def test_upload_file_no_file_part(self):
        response = self.app.post('/upload', content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "No file part")

    def test_upload_file_no_selected_file(self):
        response = self.app.post(
            '/upload',
            content_type='multipart/form-data',
            data={'file': (BytesIO(b''), '')}
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json()['error'], "No selected file")

    @patch('app.pd.read_csv')
    def test_upload_file_invalid_csv(self, mock_read_csv):
        mock_read_csv.side_effect = pd.errors.ParserError("Error parsing CSV")

        data_csv = "this is not a valid CSV file"
        mock_csv = (BytesIO(data_csv.encode()), "mock.csv")

        response = self.app.post(
            '/upload',
            content_type='multipart/form-data',
            data={'file': mock_csv}
        )

        self.assertEqual(response.status_code, 500)
        response_data = response.get_json()
        self.assertIn('error', response_data)
        self.assertEqual(response_data['error'], "Error parsing CSV")

class EvaluationTestCase(unittest.TestCase):
    def test_evaluate_quality_high(self):
        metrics = {
            "BLEU": 0.6,
            "ROUGE-1": 0.7,
            "ROUGE-L": 0.7,
            "METEOR": 0.6,
            "TER": 0.3,
            "WER": 0.2
        }
        weights = {
            "BLEU": 1,
            "ROUGE-1": 1,
            "ROUGE-L": 1,
            "METEOR": 1,
            "TER": 1,
            "WER": 1
        }
        result = evaluate_quality(metrics, weights)
        self.assertEqual(result, "high")

    def test_evaluate_quality_medium(self):
        metrics = {
            "BLEU": 0.4,
            "ROUGE-1": 0.5,
            "ROUGE-L": 0.5,
            "METEOR": 0.3,
            "TER": 0.4,
            "WER": 0.3
        }
        weights = {
            "BLEU": 1,
            "ROUGE-1": 1,
            "ROUGE-L": 1,
            "METEOR": 1,
            "TER": 1,
            "WER": 1
        }
        result = evaluate_quality(metrics, weights)
        self.assertEqual(result, "medium")

    def test_evaluate_quality_low(self):
        metrics = {
            "BLEU": 0.1,
            "ROUGE-1": 0.2,
            "ROUGE-L": 0.2,
            "METEOR": 0.1,
            "TER": 0.6,
            "WER": 0.5
        }
        weights = {
            "BLEU": 1,
            "ROUGE-1": 1,
            "ROUGE-L": 1,
            "METEOR": 1,
            "TER": 1,
            "WER": 1
        }
        result = evaluate_quality(metrics, weights)
        self.assertEqual(result, "low")

    def test_evaluate_individual_quality_high(self):
        result = evaluate_individual_quality(0.6, "BLEU")
        self.assertEqual(result, "high")

    def test_evaluate_individual_quality_medium(self):
        result = evaluate_individual_quality(0.4, "BLEU")
        self.assertEqual(result, "medium")

    def test_evaluate_individual_quality_low(self):
        result = evaluate_individual_quality(0.2, "BLEU")
        self.assertEqual(result, "low")

    def test_evaluate_individual_quality_high_ter(self):
        result = evaluate_individual_quality(0.3, "TER")
        self.assertEqual(result, "high")

    def test_evaluate_individual_quality_low_ter(self):
        result = evaluate_individual_quality(0.6, "TER")
        self.assertEqual(result, "low")

if __name__ == '__main__':
    unittest.main(verbosity=2)
