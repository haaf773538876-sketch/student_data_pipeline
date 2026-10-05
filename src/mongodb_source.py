import pandas as pd
from pymongo import MongoClient
import logging

def extract_mongodb(uri="mongodb://localhost:27017/", db_name="university_ai", col_name="students"):
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=2000)
        client.admin.command('ping')
        db = client[db_name]
        collection = db[col_name]
        
        # استخراج جميع السجلات بدون حقل _id
        records = list(collection.find({}, {"_id": 0}))
        if not records:
            return pd.DataFrame()
            
        # تسوية البيانات المتداخلة (Flattening) لتصبح أعمدة مسطحة
        df = pd.json_normalize(records)
        logging.info(f"تم استخراج وتسوية {len(df)} سجل من MongoDB.")
        return df
    except Exception as e:
        logging.error(f"خطأ في استخراج بيانات MongoDB: {e}")
        return pd.DataFrame()