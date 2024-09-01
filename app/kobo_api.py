import requests
from sqlalchemy.orm import Session
from .models import KoboRecord
from sqlalchemy.dialects.mysql import insert
from sqlalchemy import func, update

def extract_data_from_kobo(limit=1000, offset=0):
    url = f"https://kf.kobotoolbox.org/api/v2/assets/aW9w8jHjn4Cj8SSQ5VcojK/data.json?limit={limit}&offset={offset}"
    headers = {
        'Authorization': 'Token f24b97a52f76779e97b0c10f80406af5e9590eaf',
        'Cookie': 'django_language=en'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to extract data: {response.status_code}")

def process_kobo_data(data):
    processed_data = []
    for record in data.get('results', []):
        processed_record = {
            'kobo_id': record.get('_id'),
            'survey_date': record.get('cd_survey_date'),
            'unique_id': record.get('sec_a/unique_id'),
            'country': record.get('sec_a/cd_biz_country_name'),
            'region': record.get('sec_a/cd_biz_region_name'),
            'bda_name': record.get('sec_b/bda_name'),
            'cohort': record.get('sec_b/cd_cohort'),
            'program': record.get('sec_b/cd_program'),
            'client_name': record.get('sec_c/cd_client_name'),
            'client_id': record.get('sec_c/cd_client_id_manifest'),
            'location': record.get('sec_c/cd_location'),
            'phone': record.get('sec_c/cd_clients_phone'),
            'gender': record.get('sec_c/cd_gender'),
            'age': record.get('sec_c/cd_age'),
            'nationality': record.get('sec_c/cd_nationality'),
            'education': record.get('sec_c/cd_education'),
            'business_status': record.get('group_mx5fl16/cd_biz_status'),
            'submission_time': record.get('_submission_time')
        }
        processed_data.append(processed_record)
    length = len(processed_data)
    print(f"The length of the array processed_data is: {length}")  
    return processed_data

def save_records_to_db(db: Session, records):
    stmt = insert(KoboRecord).values(records)
    
    # Manually set fields that should be updated
    update_data = {
        key: stmt.inserted[key] for key in stmt.inserted._columns.keys() 
        if key not in ['id', 'kobo_id', 'inserted_at']
    }
    
    # Handle the updated_at field separately to set it to the current time
    update_data['updated_at'] = func.now()

    stmt = stmt.on_duplicate_key_update(**update_data)
    
    try:
        result = db.execute(stmt)
        db.commit()
        return result.fetchall()
    except Exception as e:
        db.rollback()
        print(f"An error occurred while saving records: {e}")
        return None

def fetch_and_save_data(db: Session, batch_size=1000):
    offset = 0
    while True:
        data = extract_data_from_kobo(limit=batch_size, offset=offset)
        processed_data = process_kobo_data(data)
        
        if not processed_data:
            break
        
        save_records_to_db(db, processed_data)
        
        if len(processed_data) < batch_size:
            break
        
        offset += batch_size