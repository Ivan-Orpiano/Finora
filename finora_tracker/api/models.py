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
    

class Expense(models.Model):
     """A single expense entry.
    Daily, monthly, quarterly, semi-annual and yearly breakdowns are all
    derived from `date` at query time (see api/utils.py) — there is
    deliberately no separate table per period, since that would just be the
    same rows duplicated and would go stale the moment an expense is edited.
    """
    
owner = models.ForeignKey(
    settings.AUTH_USER_MODEL,
    on_delete=models.CASCADE,
    related_name="expenses",
    )
category = models.ForeignKey(
    Category,
    on_delete=models.SET_NULL,
    null = True,
    blank = True,
    related_name="expenses",
    )
title = models.CharField(max_length=150)
amount = models.DecimalField(
    max_digits=12,
    decimal_places=2,
    validators=[MinValueValidator(Decimal("0.01"))],
    )
date = models.DataField(help_text = "Date the expense was incurred.")
notes = models.TextField(blank=True)
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)

class Meta:
    ordering = ["-date", "-created_at"]
    indexes = [models.Index(fields = ["owner", "date"]),]
    
def __str__(self):
    return f"{self.title} - {self.amount} on {self.date}"

class SavingsGoal(models.Model):
    """ A savings target the user is tracking progress toward the savings tracker"""
    
