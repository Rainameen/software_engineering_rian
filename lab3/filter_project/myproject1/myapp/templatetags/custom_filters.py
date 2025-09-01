import re
from django import template
from django.utils.safestring import mark_safe
from datetime import datetime
from django.utils import timezone
from collections import Counter

register = template.Library()

@register.filter
def highlight_keywords(text, keywords):
    """
    فلتر متقدم لتحديد الكلمات المفتاحية في النص مع إحصاءات
    يقبل قائمة من الكلمات المفتاحية ويميزها بألوان مختلفة
    """
    if not text or not keywords:
        return text
    
    # تحويل النص إلى قائمة كلمات مع الحفاظ على المسافات والترقيم
    words = re.findall(r'\b\w+\b|[^\w\s]', text, re.UNICODE)
    
    # إنشاء ألوان مختلفة لكل كلمة مفتاحية
    colors = [
        "#FF5733", "#33FF57", "#3357FF", "#F033FF", "#FF33A1",
        "#33FFF6", "#FFD833", "#33FF96", "#8333FF", "#FF9633"
    ]
    
    keyword_colors = {}
    for i, keyword in enumerate(keywords):
        keyword_colors[keyword.lower()] = colors[i % len(colors)]
    
    # تمييز الكلمات المفتاحية
    highlighted_words = []
    keyword_count = Counter()
    
    for word in words:
        lower_word = word.lower()
        if any(keyword.lower() == lower_word for keyword in keywords):
            keyword = next((k for k in keywords if k.lower() == lower_word), word)
            color = keyword_colors[keyword.lower()]
            highlighted_words.append(f'<mark style="background-color: {color}">{word}</mark>')
            keyword_count[keyword] += 1
        else:
            highlighted_words.append(word)
    
    # إعادة بناء النص مع الكلمات المميزة
    highlighted_text = ''.join(highlighted_words)
    
    # إنشاء إحصاءات الكلمات المفتاحية
    stats_html = '<div class="keyword-stats"><h3>إحصاءات الكلمات المفتاحية:</h3><ul>'
    for keyword, count in keyword_count.items():
        color = keyword_colors[keyword.lower()]
        stats_html += f'<li><span style="background-color: {color}; padding: 2px 5px; border-radius: 3px;">{keyword}</span>: ظهرت {count} مرات</li>'
    stats_html += '</ul></div>'
    
    return mark_safe(highlighted_text + stats_html)

@register.filter
def relative_date_ar(value):
    if not isinstance(value, datetime):
        return value

    now = timezone.now()
    diff = now - value
    seconds = diff.total_seconds()

    def arabic_time_unit(unit, count):
        if count == 0:
            return ""
        elif count == 1:
            return f"1 {unit}"
        elif count == 2:
            return f"2 {unit}ان"
        elif 3 <= count <= 10:
            return f"{count} {unit}ات"
        else:
            return f"{count} {unit}"

    if seconds >= 0:
        # الماضي
        if seconds < 60:
            return f"منذ {int(seconds)} ثانية"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"منذ {arabic_time_unit('دقيقة', minutes)}"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"منذ {arabic_time_unit('ساعة', hours)}"
        elif seconds < 2592000:
            days = int(seconds // 86400)
            return f"منذ {arabic_time_unit('يوم', days)}"
        elif seconds < 31104000:
            months = int(seconds // 2592000)
            return f"منذ {arabic_time_unit('شهر', months)}"
        else:
            years = int(seconds // 31104000)
            return f"منذ {arabic_time_unit('سنة', years)}"
    else:
        # المستقبل
        seconds = abs(seconds)
        if seconds < 60:
            return f"بعد {int(seconds)} ثانية"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"بعد {arabic_time_unit('دقيقة', minutes)}"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"بعد {arabic_time_unit('ساعة', hours)}"
        elif seconds < 2592000:
            days = int(seconds // 86400)
            return f"بعد {arabic_time_unit('يوم', days)}"
        elif seconds < 31104000:
            months = int(seconds // 2592000)
            return f"بعد {arabic_time_unit('شهر', months)}"
        else:
            years = int(seconds // 31104000)
            return f"بعد {arabic_time_unit('سنة', years)}"