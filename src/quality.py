import pandas as pd
import logging
from pathlib import Path

def validate_and_filter(df, rejected_path):
    logging.info("بدء فحص قواعد جودة البيانات (Data Quality Rules)...")
    
    rejected_records = []
    valid_indices = []

    # المرور على كل صف للتحقق من الشروط
    for index, row in df.iterrows():
        errors = []
        
        # Rule 3: 16 <= age <= 80
        if pd.notna(row.get('age')) and not (16 <= row['age'] <= 80):
            errors.append("Invalid Age")
        
        # Rule 4: 0 <= GPA <= 4
        if pd.notna(row.get('gpa')) and not (0 <= row['gpa'] <= 4):
            errors.append("Invalid GPA")
            
        # Rule 5: 0 <= attendance <= 100
        if pd.notna(row.get('attendance')) and not (0 <= row['attendance'] <= 100):
            errors.append("Invalid Attendance")
            
        # Rule 6: 0 <= score <= 100
        if pd.notna(row.get('average_score')) and not (0 <= row['average_score'] <= 100):
            errors.append("Invalid Score")

        # إذا كان هناك أخطاء، نرفقها كسبب للرفض
        if errors:
            row_copy = row.copy()
            row_copy['error_reason'] = " | ".join(errors)
            rejected_records.append(row_copy)
        else:
            valid_indices.append(index)
    
    # فصل البيانات السليمة
    valid_df = df.loc[valid_indices].copy()
    
    # حفظ البيانات المرفوضة في ملف خاص
    if rejected_records:
        rejected_df = pd.DataFrame(rejected_records)
        rejected_path.parent.mkdir(parents=True, exist_ok=True)
        rejected_df.to_csv(rejected_path, index=False)
        logging.warning(f"تم عزل {len(rejected_df)} سجل غير صالح وحفظها في {rejected_path}")
    else:
        logging.info("جميع السجلات صالحة.")
        
    return valid_df