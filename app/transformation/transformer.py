import pandas as pd
import logging

logger = logging.getLogger(__name__)

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    تحويل البيانات وإنشاء أعمدة مشتقة (Derived Columns).
    """
    logger.info("Starting Data Transformation...")
    df = df.copy()
    
    # 1. تصنيف مستوى الأداء بناءً على المعدل التراكمي (GPA)
    if "gpa" in df.columns:
        def categorize_gpa(gpa):
            if pd.isna(gpa): return "Unknown"
            if gpa >= 3.5: return "Excellent"
            elif gpa >= 3.0: return "Very Good"
            elif gpa >= 2.5: return "Good"
            elif gpa >= 2.0: return "Acceptable"
            else: return "At Risk"
            
        df["performance_level"] = df["gpa"].apply(categorize_gpa)
        
    # 2. تصنيف حالة الحضور
    if "attendance" in df.columns:
        df["attendance_status"] = df["attendance"].apply(
            lambda x: "Good" if x >= 75 else ("Low" if pd.notna(x) else "Unknown")
        )
        
    logger.info("Data Transformation completed successfully.")
    return df