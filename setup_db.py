import pandas as pd
import sqlite3
import os
import random
from pymongo import MongoClient

# --- إعداد المسارات ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW_DIR = os.path.join(BASE_DIR, "data", "raw")
DB_DIR = os.path.join(BASE_DIR, "database")

# التأكد من وجود المجلدات
os.makedirs(DATA_RAW_DIR, exist_ok=True)
os.makedirs(DB_DIR, exist_ok=True)

CSV_FILE = os.path.join(DATA_RAW_DIR, "students_raw.csv")
SQLITE_DB = os.path.join(DB_DIR, "students.db")

print("=== البدء في إنشاء البيانات الوهمية ===")

# ==========================================
# 1. إنشاء ملف CSV (يحتوي على أخطاء متعمدة)
# ==========================================
def create_csv_data():
    data = [
        {"student_id": 1001, "student_name": "Ahmed Ali", "age": 21, "major": "Computer Science", "city": "Sanaa"},
        {"student_id": 1002, "student_name": "Sara Mohammed", "age": 22, "major": "Artificial Intelligence", "city": "Aden"},
        {"student_id": 1003, "student_name": "Omar Hassan", "age": 20, "major": "Information Systems", "city": "Taiz"},
        {"student_id": 1004, "student_name": "Fatima Ahmed", "age": 23, "major": "Computer Science", "city": " sanaa "}, # مسافات زائدة وحالة أحرف
        {"student_id": 1005, "student_name": "Ali Zaid", "age": 15, "major": "IT", "city": "Sanaa"}, # عمر غير صالح (أقل من 16)
        {"student_id": 1006, "student_name": "Mona Saleh", "age": 21, "major": "AI", "city": None}, # قيمة مفقودة
        {"student_id": 1001, "student_name": "Ahmed Ali", "age": 21, "major": "Computer Science", "city": "Sanaa"}, # تكرار (Duplicate)
        {"student_id": None, "student_name": "Unknown", "age": 25, "major": "IT", "city": "Ibb"} # ID مفقود
    ]
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)
    print(f"[✓] تم إنشاء ملف CSV: {CSV_FILE}")

# ==========================================
# 2. إنشاء قاعدة بيانات SQLite
# ==========================================
def create_sqlite_data():
    conn = sqlite3.connect(SQLITE_DB)
    cursor = conn.cursor()

    # إنشاء جدول الكورسات
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS courses (
            course_id INTEGER PRIMARY KEY,
            course_name TEXT,
            credit_hours INTEGER
        )
    ''')

    # إنشاء جدول التسجيل
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS enrollments (
            enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id INTEGER,
            course_id INTEGER,
            semester TEXT,
            score INTEGER
        )
    ''')

    # إدخال بيانات الكورسات
    courses = [
        (101, 'Python Programming', 3),
        (102, 'Data Structures', 3),
        (103, 'Artificial Intelligence', 4)
    ]
    cursor.executemany('INSERT OR IGNORE INTO courses VALUES (?, ?, ?)', courses)

    # إدخال بيانات التسجيل للطلاب
    enrollments = [
        (1001, 101, 'Fall 2026', 85),
        (1002, 102, 'Fall 2026', 92),
        (1003, 103, 'Fall 2026', 78),
        (1004, 101, 'Fall 2026', 110), # درجة غير صالحة (>100)
        (1005, 102, 'Fall 2026', 60),
        (1006, 103, 'Fall 2026', 45)
    ]
    # مسح البيانات القديمة إن وجدت لتجنب التكرار عند إعادة التشغيل
    cursor.execute('DELETE FROM enrollments')
    cursor.executemany('INSERT INTO enrollments (student_id, course_id, semester, score) VALUES (?, ?, ?, ?)', enrollments)

    conn.commit()
    conn.close()
    print(f"[✓] تم إنشاء قاعدة بيانات SQLite: {SQLITE_DB}")

# ==========================================
# 3. إنشاء بيانات MongoDB
# ==========================================
def create_mongodb_data():
    try:
        # تأكد من تشغيل MongoDB محلياً على منفذ 27017
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=2000)
        client.admin.command('ping') # اختبار الاتصال
        
        db = client["university_ai"]
        collection = db["students"]
        
        # مسح البيانات القديمة لتجنب التكرار
        collection.delete_many({})

        # بيانات شبه مهيكلة للطلاب
        students_mongo = [
            {
                "student_id": 1001,
                "academic": {"gpa": 3.45, "attendance": 92},
                "status": "Active",
                "skills": ["Python", "SQL"]
            },
            {
                "student_id": 1002,
                "academic": {"gpa": 3.80, "attendance": 96},
                "status": "Active",
                "skills": ["Python", "Pandas"]
            },
            {
                "student_id": 1003,
                "academic": {"gpa": 2.10, "attendance": 65},
                "status": "At Risk",
                "skills": ["Networking"]
            },
            {
                "student_id": 1004,
                "academic": {"gpa": 4.5, "attendance": 100}, # GPA غير صالح (>4)
                "status": "Active",
                "skills": ["C++"]
            },
            {
                "student_id": 1005,
                "academic": {"gpa": 2.50, "attendance": 110}, # حضور غير صالح (>100)
                "status": "Active",
                "skills": ["HTML"]
            },
            {
                "student_id": 1006,
                "academic": {"gpa": None, "attendance": 80}, # GPA مفقود
                "status": "Active",
                "skills": ["Design"]
            }
        ]
        
        collection.insert_many(students_mongo)
        print("[✓] تم إنشاء مجموعة البيانات في MongoDB بنجاح.")
        
    except Exception as e:
        print(f"[X] فشل الاتصال أو إدراج البيانات في MongoDB. تأكد من أن الخدمة تعمل. الخطأ: {e}")

if __name__ == "__main__":
    create_csv_data()
    create_sqlite_data()
    create_mongodb_data()
    print("=== اكتمل إنشاء البيانات! ===")
    