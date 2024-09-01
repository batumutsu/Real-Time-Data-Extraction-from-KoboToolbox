import unittest
from app.kobo_api import extract_data_from_kobo
from app.models import KoboRecord
from app.database import init_db, get_db

class TestApp(unittest.TestCase):
    def setUp(self):
        init_db()
        self.db = next(get_db())

    def test_extract_data_from_kobo(self):
        data = extract_data_from_kobo()
        self.assertIsNotNone(data)
        self.assertIn('results', data)

    def test_save_record(self):
        record = {
            '_id': 'test_id',
            'data': {'field1': 'value1', 'field2': 'value2'}
        }
        new_record = KoboRecord(kobo_id=record['_id'], data=record)
        self.db.add(new_record)
        self.db.commit()

        saved_record = self.db.query(KoboRecord).filter(KoboRecord.kobo_id == 'test_id').first()
        self.assertIsNotNone(saved_record)
        self.assertEqual(saved_record.data, record)

if __name__ == '__main__':
    unittest.main()