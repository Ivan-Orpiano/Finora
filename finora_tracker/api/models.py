from django.db import models

from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models

class Category(models.Model):
    """An expense category owned by a single user"""
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="categories",
    )
    name = models.CharField(max_length=100)
    color = models.CharField(
        max_length=7,
        default="#6366F1",
        help_text="Hex color the frontend uses to tag this category, e.g. #6366F1.",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ["name"]
        unique_together = ("owner", "name")
        verbose_name_plural = "categories"
        
    def __str__(self):
        return self.name
    
    
    