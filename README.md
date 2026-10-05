# Student Data Integration & ETL Pipeline

## 1. Project Overview
هذا المشروع عبارة عن مسار بيانات هندسي (Data Engineering Pipeline) متكامل، يطبق بنية معمارية هجينة تجمع بين قواعد البيانات العلائقية (Structured Data) وقواعد البيانات غير العلائقية (Semi-structured Data عبر MongoDB). يهدف المشروع إلى استخراج بيانات الطلاب من مصادر مختلفة، تسويتها وتنظيفها، ثم دمجها لإنتاج مجموعة بيانات (Dataset) موحدة وجاهزة لنماذج الذكاء الاصطناعي (ML-ready Dataset)، مع عزل السجلات الخاطئة.

## 2. Architecture
تم تصميم المشروع ببنية حزم (Packages) احترافية تتبع مسار (Source -> PyMongo/SQLite -> Pandas -> ML Data):
- `app/sources/`: وحدات استخراج البيانات (CSV, API, SQLite, MongoDB).
- `app/transformation/`: وحدات تنظيف وتحويل وتسوية (Flattening) البيانات المتداخلة.
- `app/validation/`: قواعد جودة البيانات وعزل الأخطاء.
- `data/`: مجلد يحوي البيانات الخام، المعالجة، والمرفوضة.
- `database/`: يحتوي على قاعدة بيانات SQLite.
- `logs/`: يحتوي على سجلات التتبع (Pipeline Logs).
- `main.py`: نقطة الإطلاق لتشغيل المسار بالكامل.

## 3. Data Sources
تم جمع البيانات من 4 مصادر مختلفة بربطها عبر المفتاح المشترك `student_id`:
1. **CSV File**: بيانات الطلاب الأساسية.
2. **SQLite Database**: بيانات علائقية (Relational) للكورسات والدرجات.
3. **MongoDB**: بيانات شبه مهيكلة (Semi-structured) تعتمد على نموذج المستندات (Document Model) وتتضمن حقولاً متداخلة (Nested) مثل `academic` ومصفوفات (Arrays) مثل `skills`.
4. **REST API**: بيانات إضافية عبر طلبات HTTP.

## 4. ETL Pipeline
- **Extract (الاستخراج)**: جلب البيانات باستخدام `pandas`, `sqlite3`, و `PyMongo` لاستخراج مستندات BSON من MongoDB.
- **Transform (التحويل والتسوية)**: استخدام دالة `pd.json_normalize()` لحل مشكلة الحقول المتداخلة (Nested Fields Problem) القادمة من MongoDB، وتحويلها إلى أعمدة مسطحة، بالإضافة إلى اشتقاق أعمدة جديدة مثل `performance_level`.
- **Clean (التنظيف)**: إزالة التكرارات، التعامل مع القيم المفقودة، وتوحيد النصوص.
- **Integrate (الدمج)**: دمج الجداول الأربعة باستخدام Left Join بناءً على `student_id`.
- **Validate (التحقق)**: تطبيق قواعد جودة البيانات (Data Quality) وفصل السجلات المرفوضة.
- **Load (التحميل)**: حفظ البيانات السليمة في `final_dataset.csv`.

## 5. Data Quality Rules
تم تطبيق القواعد التالية لضمان جودة البيانات:
- `student_id` يجب أن يكون موجوداً وفريداً.
- `age` يجب أن يكون بين 16 و 80.
- `gpa` يجب أن يكون بين 0 و 4.
- `attendance` و `score` يجب أن تكون بين 0 و 100.

## 6. Installation & Running
لتشغيل المشروع محلياً:
1. تثبيت المتطلبات:
   ```bash
   pip install -r requirements.txt