import requests
import pandas as pd
import logging

def extract_api(url):
    try:
        # استخدام API وهمي لجلب بيانات إضافية
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # تحويل JSON إلى DataFrame
        df = pd.DataFrame(data)
        
        # لأن API العام لا يحتوي على student_id، سنعيد تسمية عمود 'id' لربطه لاحقاً
        if 'id' in df.columns:
            df.rename(columns={'id': 'student_id'}, inplace=True)
            
        logging.info(f"تم استخراج {len(df)} سجل من API.")
        return df
    except Exception as e:
        logging.error(f"خطأ في استخراج بيانات API: {e}")
        return pd.DataFrame()