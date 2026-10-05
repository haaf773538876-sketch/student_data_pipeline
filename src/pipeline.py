import pandas as pd
import logging

def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        logging.info(f"تم تحميل {len(df)} سجل من ملف CSV.")
        return df
    except Exception as e:
        logging.error(f"خطأ في قراءة ملف CSV: {e}")
        return pd.DataFrame()

def convert_data_types(df):
    if 'student_id' in df.columns:
        df['student_id'] = pd.to_numeric(df['student_id'], errors='coerce')
    if 'age' in df.columns:
        df['age'] = pd.to_numeric(df['age'], errors='coerce')
    return df

def clean_data(df):
    logging.info("بدء تنظيف البيانات الأساسية...")
    
    # 1. إزالة السجلات التي لا تحتوي على رقم جامعي
    df = df.dropna(subset=['student_id'])
    
    # 2. إزالة التكرارات بناءً على الرقم الجامعي
    df = df.drop_duplicates(subset=['student_id'], keep='first')
    
    # 3. توحيد النصوص (إزالة المسافات الزائدة وتوحيد حالة الأحرف لاسم المدينة)
    if 'city' in df.columns:
        df['city'] = df['city'].astype(str).str.strip().str.title()
        df['city'] = df['city'].replace({'Nan': 'Unknown', 'None': 'Unknown'})
        
    logging.info(f"اكتمل التنظيف. عدد السجلات المتبقية: {len(df)}")
    return df

def validate_data(df):
    # سنكتب قواعد عزل البيانات المرفوضة في الخطوة القادمة
    pass