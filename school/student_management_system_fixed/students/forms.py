from django import forms
from django.core.exceptions import ValidationError
from .models import Student

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'age', 
            'gender', 'student_id', 'year', 'gpa', 'address', 
            'photo', 'is_active'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter first name'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter last name'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter email address'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter phone number'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '16',
                'max': '100'
            }),
            'gender': forms.Select(attrs={
                'class': 'form-select'
            }),
            'student_id': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter student ID'
            }),
            'year': forms.Select(attrs={
                'class': 'form-select'
            }),
            'gpa': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'min': '0',
                'max': '4'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter address'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            })
        }

    def clean_student_id(self):
        student_id = self.cleaned_data['student_id']
        if Student.objects.filter(student_id=student_id).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A student with this ID already exists.")
        return student_id

    def clean_email(self):
        email = self.cleaned_data['email']
        if Student.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A student with this email already exists.")
        return email

class StudentSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Search by name, email, or student ID...'
        })
    )
    
    year = forms.ChoiceField(
        choices=[('', 'All Years')] + Student.YEAR_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    gender = forms.ChoiceField(
        choices=[('', 'All Genders')] + Student.GENDER_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )
    
    is_active = forms.ChoiceField(
        choices=[('', 'All Status'), ('True', 'Active'), ('False', 'Inactive')],
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-select'
        })
    )



from .models import Grade

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ["score"]
        widgets = {
            "score": forms.NumberInput(attrs={
                "class": "form-control",
                "min": "0",
                "max": "100",
                "placeholder": "أدخل الدرجة (0-100)"
            })
        }


