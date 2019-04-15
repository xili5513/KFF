from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

RATING_CHOICES = (
    ('Best', 'Best'),
    ('Good', 'Good'),
    ('Avoid', 'Avoid'),
)


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    rating = models.CharField(max_length=20, choices=RATING_CHOICES, default='Best', blank=True, null=True)
    product_name = models.CharField(max_length=400, blank=True, default='')
    product_category = models.CharField(max_length=400, blank=True, default='')
    accreditation = models.CharField(max_length=400, blank=True, default='')
    availability = models.CharField(max_length=1000, blank=True, default='')
    location = models.CharField(max_length=400, blank=True, default='')
    address = models.CharField(max_length=400, blank=True, default='')
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE)

    class Meta:
        ordering = ('created',)

