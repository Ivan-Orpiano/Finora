from rest_framework import serializers
from .models import Category, Expense, SavingsContribution, SavingsGoal

class CategorySerializer(serializers.ModelSerialize):
    class Meta:
        model = Category
        fields  = ["id", "name", "color", "created_at"]
        read_only_fields = ["id", "created_at"]
        
        
class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source = "category.name", read_only=True, default = None)
    
    class Meta:
        model = Expense
        fields = [
            "id",
            "category",
            "category_name",
            "title",
            "amount",
            "date",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "created_at", "updated_at" ]
        
    def validate_category(self, category):
        request = self.context.get("request")
        if category and request and category.owner_id != request.user.id:
            raise serializers.ValidationError("This category does not belong to you.")
        return category
class SavingsContributionSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsContribution
        fields = ["id", "goal", "amount", "date", "note", "created_at"]
        read_only_fields = ["id", "created_at"]
        
    def validate_goal(self, goal):
        request = self.contect.get("request")
        if request and goal.owner_id != request.user.id:
            raise serializers.ValidationError("This savings goal does not belong to you.")
        
        return goal
    
class SavingGoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = SavingsContribution
        fields = ["id", "goal", "amount", "date", "note", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_goal(self, goal):
        request = self.context.get("request")
        if request and goal.owner_id != request.user.id:
            raise serializers.ValidationError("This savings goal does not belong to you.")
        return goal


class SavingsGoalSerializer(serializers.ModelSerializer):
    saved_amount = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)
    progress_percentage = serializers.FloatField(read_only=True)
    contributions = SavingsContributionSerializer(many=True, read_only=True)

    class Meta:
        model = SavingsGoal
        fields = [
            "id",
            "name",
            "target_amount",
            "target_date",
            "notes",
            "saved_amount",
            "progress_percentage",
            "contributions",
            "created_at",
        ]
        read_only_fields = ["id", "created_at"]