from django.shortcuts import render
from django.db.models import Sum
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Category, Expense, SavingsContribution, SavingsGoal
from .permissions import IsOwner
from .serializers import (
    CategorySerializer,
    ExpenseSerializer,
    SavingsContributinSerializer,
    SavingsGoalSerializer,
)
from .utils import PERIOD_CHOICES, annotate_period



