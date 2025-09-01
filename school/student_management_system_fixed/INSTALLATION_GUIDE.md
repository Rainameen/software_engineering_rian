# دليل التثبيت - نظام إدارة الطلاب

## حل مشكلة `ModuleNotFoundError: No module named 'crispy_forms'`

### الطريقة الأولى: التثبيت التلقائي
```bash
python install_requirements.py
```

### الطريقة الثانية: التثبيت اليدوي
```bash
pip install django-crispy-forms
pip install crispy-bootstrap5
pip install Django
pip install Pillow
pip install reportlab
```

### الطريقة الثالثة: استخدام requirements.txt
```bash
pip install -r requirements.txt
```

## خطوات التشغيل

1. **تثبيت المتطلبات**
   ```bash
   pip install -r requirements.txt
   ```

2. **تشغيل الترحيلات**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

3. **إنشاء بيانات تجريبية (اختياري)**
   ```bash
   python create_sample_data.py
   ```

4. **إنشاء مستخدم مدير (اختياري)**
   ```bash
   python manage.py createsuperuser
   ```

5. **تشغيل الخادم**
   ```bash
   python manage.py runserver
   ```

6. **زيارة الموقع**
   - الموقع الرئيسي: http://127.0.0.1:8000/
   - لوحة الإدارة: http://127.0.0.1:8000/admin/

## حل المشاكل الشائعة

### مشكلة `ModuleNotFoundError`
إذا واجهت هذه المشكلة، تأكد من:
1. تفعيل البيئة الافتراضية (إذا كنت تستخدمها)
2. تثبيت جميع المتطلبات
3. استخدام نفس إصدار Python

### مشكلة قاعدة البيانات
```bash
python manage.py makemigrations students
python manage.py migrate
```

### مشكلة الملفات الثابتة
```bash
python manage.py collectstatic
```

## متطلبات النظام
- Python 3.8+
- Django 4.0+
- متصفح ويب حديث

## الدعم
إذا واجهت أي مشاكل، تحقق من:
1. إصدار Python المستخدم
2. تثبيت جميع المتطلبات
3. صحة إعدادات Django

