# Student Management System

A comprehensive Django-based student management system with modern UI design and advanced QuerySet operations demonstration.

## 🌟 Features

### Core CRUD Operations
- ✅ **Create** - Add new students with detailed information
- ✅ **Read** - View all students with advanced search and filtering
- ✅ **Update** - Edit student information with form validation
- ✅ **Delete** - Remove students with confirmation dialog

### Advanced QuerySet Operations
- 📊 **Order By** - Sort students ascending/descending
- 🔍 **Contains Search** - Find students by partial name match
- 📋 **In Query** - Filter by multiple values
- 📏 **Range Query** - Filter by age or GPA range
- 🎯 **Exact Match** - Precise field matching
- ❌ **Exclude** - Remove specific records from results
- 🔀 **Complex Queries** - Combined conditions with Q objects

### Modern UI Features
- 🎨 **Modern Design** - Clean, professional interface
- 📱 **Responsive Layout** - Works on desktop and mobile
- 📊 **Dashboard** - Statistics and charts
- 🔍 **Advanced Search** - Multiple filter options
- 📄 **Pagination** - Efficient data browsing
- 📸 **Photo Upload** - Student profile pictures
- 📈 **Data Visualization** - Charts for statistics

### Export & Reporting
- 📄 **CSV Export** - Download student data
- 📑 **PDF Reports** - Formatted student reports
- 🖨️ **Print Support** - Print-friendly pages

## 🚀 Installation

### Prerequisites
- Python 3.8+
- Django 4.0+
- Modern web browser

### Setup Instructions

1. **Clone or extract the project**
   ```bash
   cd student_management_system
   ```

2. **Create virtual environment (recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main application: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
student_management_system/
├── manage.py                 # Django management script
├── requirements.txt          # Project dependencies
├── README.md                # This file
├── db.sqlite3               # SQLite database (created after migration)
├── student_management_system/
│   ├── __init__.py
│   ├── settings.py          # Django settings
│   ├── urls.py              # Main URL configuration
│   ├── wsgi.py              # WSGI configuration
│   └── asgi.py              # ASGI configuration
├── students/                # Main application
│   ├── __init__.py
│   ├── admin.py             # Admin interface configuration
│   ├── apps.py              # App configuration
│   ├── models.py            # Student model
│   ├── views.py             # View functions
│   ├── urls.py              # App URL patterns
│   ├── forms.py             # Django forms
│   └── migrations/          # Database migrations
├── templates/               # HTML templates
│   ├── base.html            # Base template
│   └── students/            # Student-specific templates
│       ├── dashboard.html
│       ├── student_list.html
│       ├── student_detail.html
│       ├── student_form.html
│       ├── student_confirm_delete.html
│       └── advanced_queries.html
├── static/                  # Static files (CSS, JS, images)
│   ├── css/
│   ├── js/
│   └── images/
└── media/                   # User uploads
    └── student_photos/      # Student profile photos
```

## 🎯 Usage Guide

### Dashboard
- View system statistics and charts
- Quick access to main functions
- Visual representation of student data

### Student Management
1. **Add Student**: Click "Add New Student" and fill the form
2. **View Students**: Browse paginated list with search/filter options
3. **Student Details**: Click on any student to view full information
4. **Edit Student**: Use the edit button on student detail page
5. **Delete Student**: Confirmation required for safety

### Advanced Queries
Visit the "Query Examples" page to see demonstrations of:
- Sorting operations
- Text search with contains
- Multiple value filtering
- Range queries
- Complex conditions

### Export Data
- **CSV Export**: Download all student data in CSV format
- **PDF Report**: Generate formatted PDF reports

## 🛠️ Technical Details

### Technologies Used
- **Backend**: Django 5.2.5
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Database**: SQLite (default), PostgreSQL compatible
- **Charts**: Chart.js
- **Icons**: Font Awesome
- **Forms**: Django Crispy Forms with Bootstrap 5

### Key Components

#### Models
- **Student Model**: Comprehensive student information with validation
- Fields: Personal info, contact details, academic data, photos

#### Views
- **Function-based views** for all CRUD operations
- **Advanced QuerySet demonstrations**
- **Export functionality** (CSV/PDF)
- **AJAX endpoints** for dynamic content

#### Templates
- **Responsive design** with modern UI
- **Component-based structure**
- **Accessibility features**
- **Print-friendly styles**

## 🎨 Design Features

### Color Scheme
- **Primary**: #2563eb (Modern Blue)
- **Secondary**: #10b981 (Mint Green)
- **Accent**: #f59e0b (Warm Orange)
- **Neutral**: #6b7280 (Medium Gray)
- **Background**: #f8fafc (Light Blue-Gray)

### Typography
- **Primary Font**: Inter (Clean, modern)
- **Secondary Font**: Roboto (Readable, professional)

### UI Elements
- **Cards**: Elevated design with subtle shadows
- **Buttons**: Rounded corners with hover effects
- **Forms**: Clean layout with validation feedback
- **Tables**: Striped rows with hover states
- **Charts**: Interactive data visualization

## 📊 QuerySet Examples Explained

The system demonstrates all QuerySet operations from the Software Engineering Lab 5 presentation:

1. **Order By (Ascending)**: `Student.objects.order_by('first_name')`
2. **Order By (Descending)**: `Student.objects.order_by('-first_name')`
3. **Contains**: `Student.objects.filter(first_name__contains='a')`
4. **In Query**: `Student.objects.filter(year__in=['1', '2', '3'])`
5. **Range**: `Student.objects.filter(age__range=[18, 25])`
6. **Exact**: `Student.objects.filter(year__exact='1')`
7. **Exclude**: `Student.objects.exclude(is_active=False)`
8. **Complex**: `Student.objects.filter(Q(first_name__icontains='Malek') | Q(age__lt=23))`

## 🔧 Customization

### Adding New Fields
1. Update the `Student` model in `students/models.py`
2. Update forms in `students/forms.py`
3. Run migrations: `python manage.py makemigrations && python manage.py migrate`
4. Update templates as needed

### Styling Changes
- Modify CSS variables in `templates/base.html`
- Add custom styles in `static/css/`
- Update color scheme in the `:root` CSS variables

### Adding New Features
- Create new views in `students/views.py`
- Add URL patterns in `students/urls.py`
- Create corresponding templates

## 🐛 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   python manage.py makemigrations --empty students
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   python manage.py collectstatic
   ```

3. **Permission Errors**
   - Ensure proper file permissions
   - Check media directory write access

4. **Database Issues**
   - Delete `db.sqlite3` and re-run migrations
   - Check database connection settings

## 📝 License

This project is created for educational purposes as part of Software Engineering Lab 5.

## 👨‍💻 Developer

Created by: Malek Almosanif  
Email: almosnif1095@gmail.com  
Course: Software Engineering IT4

## 🤝 Contributing

This is an educational project. Feel free to:
- Report bugs
- Suggest improvements
- Add new features
- Improve documentation

## 📞 Support

For support or questions:
- Check the troubleshooting section
- Review Django documentation
- Contact the developer

---

**Note**: This system demonstrates Django CRUD operations and QuerySet functionality as covered in Software Engineering Lab 5. It includes modern UI design, comprehensive features, and follows Django best practices.

