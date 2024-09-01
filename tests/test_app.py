import unittest
from unittest.mock import Mock, patch
from flask import jsonify
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.kobo_api import extract_data_from_kobo, process_kobo_data, save_records_to_db
from dotenv import load_dotenv
import os
from app.models import Base, KoboRecord

load_dotenv()


class TestKoboDataProcessing(unittest.TestCase):

    DATABASE_TEST_URL = os.getenv('DATABASE_TEST_URL')

    engine = create_engine(DATABASE_TEST_URL)
    Session = sessionmaker(bind=engine)
    session = Session()
    Base.metadata.create_all(bind=engine)

    @patch('requests.get')
    def test_extract_data_from_kobo_success(self, mock_get):
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': []}
        mock_get.return_value = mock_response

        data = extract_data_from_kobo()
        self.assertEqual(data, {'results': []})

    @patch('requests.get')
    def test_extract_data_from_kobo_failure(self, mock_get):
        # Mock failed response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        with self.assertRaises(Exception) as e:
            extract_data_from_kobo()
        self.assertEqual(str(e.exception), "Failed to extract data: 404")

    def test_extract_data_from_kobo(self):
            data = extract_data_from_kobo()
            processed_data = process_kobo_data(data)
            for record in processed_data:
                # Check that response contains all required fields
                required_fields = [
                'kobo_id',
                'survey_date',
                'unique_id',
                'country',
                'region',
                'bda_name',
                'cohort',
                'program',
                'client_name',
                'client_id',
                'location',
                'phone',
                'alt_phone',
                'phone_smart_feature',
                'gender',
                'age',
                'nationality',
                'strata',
                'disability',
                'education',
                'client_status',
                'sole_income_earner',
                'responsible_people',
                'business_status',
                'business_operating',
                'submission_time'
                ]
                for field in required_fields:
                    assert field in record, f"Field '{field}' is missing from the response"

                # Optionally, check if required fields have non-null values
                non_nullable_fields = [
                'unique_id',
                'country',
                'region',
                'bda_name',
                'cohort',
                'program',
                'client_name',
                'client_id',
                'location',
                'phone',
                'phone_smart_feature',
                'gender',
                'age',
                'nationality',
                'strata',
                'education',
                'client_status',
                'responsible_people',
                'business_status',
                'submission_time'
                ]

                for field in non_nullable_fields:
                    assert record.get(field) is not None, f"Field '{field}' should not be null"

                # Optional: Validate field types if necessary
                # Example for validating integer fields
                try:
                    age_value = int(record.get('age'))
                    assert isinstance(age_value, int), "Field 'age' should be an integer"
                    responsible_people = int(record.get('responsible_people'))
                    assert isinstance(responsible_people, int), "Field 'responsible_people' should be an integer"
                    # Check that the 'disability' field is either 'Yes' or 'No'
                    disability_value = record.get('disability')
                    assert disability_value in ["Yes", "No"], "Field 'disability' should be either 'Yes' or 'No', but got '{}'".format(disability_value)
                    # Check that the 'disability' field is either 'Yes' or 'No'
                    gender_value = record.get('gender')
                    assert gender_value in ["Male", "Female"], "Field 'disability' should be either 'Yes' or 'No', but got '{}'".format(disability_value)

                except (ValueError, TypeError):
                    assert False, "Field 'age' and responsible_people should be convertible to an integer"

                # Example for validating string fields
                assert isinstance(record.get('unique_id'), str), "Field 'unique_id' should be a string"
                assert isinstance(record.get('country'), str), "Field 'country' should be a string"


    def test_process_kobo_data_empty(self):
        data = {}
        processed_data = process_kobo_data(data)
        self.assertEqual(processed_data, [])

    def test_process_kobo_data_single_record(self):
        data = {'results': [{'_id': '123', 'cd_survey_date': '2024-09-01'}]}
        processed_data = process_kobo_data(data)
        self.assertEqual(len(processed_data), 1)
        self.assertEqual(processed_data[0]['kobo_id'], '123')
        self.assertEqual(processed_data[0]['survey_date'], '2024-09-01')

    @patch('sqlalchemy.orm.Session.execute')
    def test_save_records_to_db(self, mock_execute):
        # Mock successful insert
        mock_execute.return_value = None
        db = unittest.mock.MagicMock()
        records = [{'kobo_id': '123'}]

        save_records_to_db(db, records)

        db.execute.assert_called_once()
        db.commit.assert_called_once()
    
    # def test_save_records_to_db(self):
    #     data = extract_data_from_kobo()
    #     processed_data = process_kobo_data(data)

    #     # Call the actual save function
    #     save_records_to_db(self.session, processed_data)

    #     # Verify the record was saved
    #     test_kobo_id = processed_data[0]['kobo_id']
    #     result = self.session.execute(
    #     text("SELECT * FROM kobo_records WHERE kobo_id = :test_kobo_id"),
    #     {"test_kobo_id": test_kobo_id}
    # ).fetchone()
    #     self.assertIsNotNone(result)
    #     self.assertEqual(result['kobo_id'], test_kobo_id)

    #     # Clean up
    #     self.session.rollback()  # Or delete the test records manually
    #     self.session.close()
    
    
    def test_save_records_to_db(self):
        data = extract_data_from_kobo()
        processed_data = process_kobo_data(data)

        # Call the actual save function
        save_records_to_db(self.session, processed_data)

        # Verify the record was saved
        test_kobo_id = processed_data[0]['kobo_id']

        # Use session.query() to fetch the result as a model instance
        result = self.session.query(KoboRecord).filter_by(kobo_id=test_kobo_id).first()


        # Access by position: result[0] or result['kobo_id'] depending on the column order
        self.assertIsNotNone(result)
        self.assertEqual(result.kobo_id, test_kobo_id)  # Assuming 'kobo_id' is the first column

        # Clean up
        self.session.execute(text("DELETE FROM kobo_records"))  # Delete all records
        self.session.commit()  # Commit the transaction to persist the changes

        self.session.close()



# Run the tests
if __name__ == '__main__':
    unittest.main()