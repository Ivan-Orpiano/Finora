from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import(
    CategoryViewSet,
    ExpenseViewSet,
    SavingsContributionViewSet,
    SavingsGoalViewSet,
)

router = DefaultRouter()
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"expenses", ExpenseViewSet, basename="expense")
router.register(r"savings-goals", SavingsGoalViewSet, basename="savings-goal")
router.register(
    r"savings-contributions", SavingsContributionViewSet, basename="savings-goal"
)

urlpatterns = [
    path("", include(router.urls)),
]

