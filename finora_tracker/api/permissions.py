from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """Object-level permission: a user may only see or edit their own records
        Works for models that have a direct `owner` FK (Category, expense, SavingsGoal)
        and for SavingsContribution, which is only linked to a user indirectly through `goal.owner,"""
        
    
    def has_object_permission(self, request, view, obj):
        owner = getattr(obj, "owner", None)
        if owner is None and hasattr(obj, "goal"):
            owner = obj.goal.owner
        return owner == request.user    
        
    