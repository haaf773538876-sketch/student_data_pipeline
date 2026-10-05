import sqlite3
import pandas as pd
import logging

def extract_database(db_path):
    try:
        conn = sqlite3.connect(db_path)
        # دمج جدولي الطلاب والكورسات باستخدام JOIN
        query = '''
        SELECT e.student_id, c.course_name, e.semester, e.score
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        '''
        df = pd.read_sql_query(query, conn)
        conn.close()
        logging.info(f"تم استخراج {len(df)} سجل من قاعدة بيانات SQLite.")
        return df
    except Exception as e:
        logging.error(f"خطأ في استخراج بيانات SQLite: {e}")
        return pd.DataFrame()