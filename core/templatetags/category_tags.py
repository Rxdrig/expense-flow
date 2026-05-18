from django import template
from django.utils.safestring import mark_safe

register = template.Library()

CATEGORY_META = {
    'food': {'label': 'Alimentación', 'color': '#FF7A7A', 'icon': '🍔'},
    'transport': {'label': 'Transporte', 'color': '#7AC8FF', 'icon': '🚌'},
    'entertainment': {'label': 'Entretenimiento', 'color': '#C77DFF', 'icon': '🎬'},
    'games': {'label': 'Juegos', 'color': '#FFB86B', 'icon': '🎮'},
    'subscriptions': {'label': 'Suscripciones', 'color': '#6CE0B5', 'icon': '💳'},
    'education': {'label': 'Educación', 'color': '#7ED0FF', 'icon': '📚'},
    'other': {'label': 'Otro', 'color': '#A0AEC0', 'icon': '🗂️'},
}


@register.simple_tag
def category_badge(cat_key):
    meta = CATEGORY_META.get(cat_key, CATEGORY_META['other'])
    label = meta.get('label')
    icon = meta.get('icon')
    color = meta.get('color')
    html = f'<span class="category-badge" data-cat="{cat_key}" style="background:{color};">'
    html += f'<span class="cat-icon">{icon}</span> <span class="cat-label">{label}</span></span>'
    return mark_safe(html)
