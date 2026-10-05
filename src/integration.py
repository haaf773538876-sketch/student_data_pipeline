import pandas as pd
import logging

def integrate_data(df_csv, df_api, df_db, df_mongo):
    logging.info("بدء دمج البيانات من جميع المصادر...")
    
    # الاعتماد على CSV كقاعدة أساسية (Left Join)
    integrated_df = df_csv.copy()
    
    # دمج بيانات MongoDB (تحتوي على المعدل ونسبة الحضور والمهارات)
    if not df_mongo.empty:
        integrated_df = pd.merge(integrated_df, df_mongo, on='student_id', how='left')
        
    # دمج بيانات SQLite 
    if not df_db.empty:
        # تجميع الدرجات في متوسط واحد لكل طالب لمنع تضاعف السجلات
        db_grouped = df_db.groupby('student_id')['score'].mean().reset_index()
        db_grouped.rename(columns={'score': 'average_score'}, inplace=True)
        integrated_df = pd.merge(integrated_df, db_grouped, on='student_id', how='left')
        
    # دمج بيانات API الوهمية (أخذ بعض الأعمدة كمثال إضافي)
    if not df_api.empty and 'student_id' in df_api.columns:
        api_subset = df_api[['student_id', 'username']] if 'username' in df_api.columns else df_api
        integrated_df = pd.merge(integrated_df, api_subset, on='student_id', how='left')
        
    logging.info(f"اكتمل الدمج بنجاح. إجمالي الأعمدة: {list(integrated_df.columns)}")
    return integrated_df