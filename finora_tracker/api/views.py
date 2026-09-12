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
    SavingsContributionSerializer,
    SavingsGoalSerializer,
)
from .utils import PERIOD_CHOICES, annotate_period


class CategoryViewSet(viewsets.ModelViewSet):
    """CRUD for expense categories. /api/categories"""
    
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class ExpenseViewSet(viewsets.ModelViewSet):
    """CRUD for expenses, plus the period-summary and by-category reports.

    /api/expenses/                         list / create
    /api/expenses/{id}/                    retrieve / update / delete
    /api/expenses/summary/?period=monthly  daily | monthly | quarterly | semiannual | yearly
    /api/expenses/by_category/             totals grouped by category

    Both report endpoints respect start_date, end_date and category
    query params, same as the list endpoint.
    """
    
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    
    def get_queryset(self):
        self.queryset = Expense.objects.filter(owner = self.request.user)
        params = self.request.query_params
        
        start_date = params.get("start_date")
        end_date = params.get("end_date")
        category_id = params.get("category")
        
        if start_date:
            queryset = queryset.filter(date__gte = start_date)
        if end_date:
            queryset = queryset.filtet(date__lte = end_date)
        if category_id:
            queryset = queryset.filter(category_id=category_id)
            
        return queryset
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context
    
    def perform_create(self, serializer):
        serializer.save(owner = self.request.user)
        
    @action(detail = False, methods=["get"])
    def summary(self, request):
        period = request.query_params.get("period", "monthly")
        if period not in PERIOD_CHOICES:
            return response(
                {"detail" : f"period must be one of {PERIOD_CHOICES}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        queryset = self.get_queryset()
        buckets = annotate_period(queryset, period)
        grand_total = queryset.aggregate(total=Sum("amount"))["total"] or 0
        
        return Response({
          "period" : period,
          "result" : buckets,
          "grand_total" : grand_total  
            }
        )
        
    @action(detail = False, methods = ["get"], url_path="by_category")
    def by_category(self, request):
        pass
        