from django.shortcuts import render, redirect
from django.contrib import messages
from .models import TextEntry

def home(request):
    """العرض الرئيسي لإدخال النص وعرض النتائج"""
    reversed_text = ""
    original_text = ""
    
    if request.method == 'POST':
        original_text = request.POST.get('text', '').strip()
        
        if original_text:
            # إنشاء إدخال جديد في قاعدة البيانات
            text_entry = TextEntry(original_text=original_text)
            text_entry.save()
            
            reversed_text = text_entry.reversed_text
            messages.success(request, 'تم عكس النص بنجاح!')
        else:
            messages.error(request, 'يرجى إدخال نص صالح.')
    
    # جلب آخر 10 إدخالات
    recent_entries = TextEntry.objects.all()[:10]
    
    context = {
        'original_text': original_text,
        'reversed_text': reversed_text,
        'recent_entries': recent_entries,
    }
    
    return render(request, 'reverser/home.html', context)

def history(request):
    """عرض تاريخ جميع النصوص المعكوسة"""
    entries = TextEntry.objects.all()
    
    context = {
        'entries': entries,
    }
    
    return render(request, 'reverser/history.html', context)
