import logging
from pathlib import Path

from src.pipeline import load_data, clean_data, convert_data_types
from src.api_source import extract_api
from src.database_source import extract_database
from src.mongodb_source import extract_mongodb
from src.integration import integrate_data
from src.transformer import transform_data
from src.quality import validate_and_filter # استدعاء دالة الجودة

# إعداد المسارات
CSV_FILE = Path("data/raw/students_raw.csv")
FINAL_OUTPUT = Path("data/processed/final_dataset.csv")
REJECTED_OUTPUT = Path("data/rejected/rejected_records.csv") # مسار المرفوضات
LOG_FILE = Path("logs/pipeline.log")

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)
logger = logging.getLogger(__name__)

def run_pipeline():
    try:
        logger.info("=== بدء تشغيل Data Pipeline ===")
        print("جاري تشغيل مسار البيانات...")
        
        # 1. الاستخراج
        df_csv = load_data(CSV_FILE)
        df_api = extract_api("https://jsonplaceholder.typicode.com/users") 
        df_db = extract_database("database/students.db")
        df_mongo = extract_mongodb()
        
        # التنظيف
        df_csv = convert_data_types(df_csv)
        df_csv = clean_data(df_csv)
        
        # 2. الدمج
        integrated_df = integrate_data(df_csv, df_api, df_db, df_mongo)
        
        # 3. التحويل
        transformed_df = transform_data(integrated_df)
        
        # 4. فحص الجودة وعزل البيانات غير الصالحة
        valid_final_df = validate_and_filter(transformed_df, REJECTED_OUTPUT)
        
        # 5. الحفظ
        FINAL_OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        valid_final_df.to_csv(FINAL_OUTPUT, index=False)
        
        logger.info("=== اكتمل مسار البيانات بنجاح! ===")
        print(f"تم التنفيذ! السجلات الصحيحة: {len(valid_final_df)}، تم حفظها في {FINAL_OUTPUT}")
        if REJECTED_OUTPUT.exists():
            print(f"تم عزل السجلات الخاطئة، راجع: {REJECTED_OUTPUT}")
            
    except Exception as e:
        logger.exception(f"فشل تشغيل Pipeline بسبب خطأ غير متوقع: {e}")
        print(f"حدث خطأ أثناء التنفيذ. راجع ملف {LOG_FILE} للتفاصيل.")

if __name__ == "__main__":
    run_pipeline()