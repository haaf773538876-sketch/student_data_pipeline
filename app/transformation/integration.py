import pandas as pd
import logging

logger = logging.getLogger(__name__)

def integrate_data(df_csv: pd.DataFrame, df_api: pd.DataFrame, df_db: pd.DataFrame) -> pd.DataFrame:
    """
    دمج البيانات من المصادر الثلاثة باستخدام student_id
    """
    logger.info("Starting Data Integration...")
    
    # إذا لم يكن لدينا بيانات الطلاب الأساسية، لا يمكننا إكمال الدمج
    if df_csv.empty:
        logger.error("CSV data is empty. Integration cannot proceed.")
        return pd.DataFrame()
        
    # نبدأ ببيانات CSV كأساس (Left Table)
    integrated_df = df_csv.copy()
    
    # دمج بيانات API باستخدام Left Join للحفاظ على كل الطلاب
    if not df_api.empty:
        integrated_df = pd.merge(integrated_df, df_api, on="student_id", how="left")
        logger.info("API data merged successfully.")
        
    # دمج بيانات قاعدة البيانات (SQLite)
    if not df_db.empty:
        integrated_df = pd.merge(integrated_df, df_db, on="student_id", how="left")
        logger.info("Database data merged successfully.")
        
    logger.info(f"Integration completed. Resulting dataset shape: {integrated_df.shape}")
    return integrated_df