import pandas as pd
import logging

def transform_data(df):
    logging.info("بدء عملية تحويل البيانات (Transformation)...")
    
    # 1. معالجة القيم المفقودة باستخدام المتوسط (Mean)
    if 'academic.gpa' in df.columns:
        gpa_mean = round(df['academic.gpa'].mean(), 2)
        df['academic.gpa'] = df['academic.gpa'].fillna(gpa_mean)
    
    if 'academic.attendance' in df.columns:
        df['academic.attendance'] = df['academic.attendance'].fillna(0)

    # 2. إنشاء أعمدة مشتقة (Derived Columns)
    def get_performance(gpa):
        if pd.isna(gpa): return 'Unknown'
        if gpa >= 3.5: return 'Excellent'
        elif gpa >= 3.0: return 'Very Good'
        elif gpa >= 2.5: return 'Good'
        elif gpa >= 2.0: return 'Acceptable'
        else: return 'At Risk'

    def get_attendance_status(att):
        if pd.isna(att): return 'Unknown'
        if att >= 75: return 'Good'
        else: return 'Low'

    if 'academic.gpa' in df.columns:
        df['performance_level'] = df['academic.gpa'].apply(get_performance)
    
    if 'academic.attendance' in df.columns:
        df['attendance_status'] = df['academic.attendance'].apply(get_attendance_status)

    # 3. توحيد أسماء الأعمدة 
    df.rename(columns={
        'academic.gpa': 'gpa',
        'academic.attendance': 'attendance',
        'student_name': 'name'
    }, inplace=True)

    logging.info("اكتملت عملية التحويل بنجاح.")
    return df