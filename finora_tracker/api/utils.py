"""Period-bucketing helpers used by ExpenseViewSet.summary().

All budget "divisions" (daily / monthly / quarterly / semi-annual / yearly)
are computed here from the `date` field at query time - there's one source
of truth (the Expense table), and every division is just a different GROUP BY.
"""

from django.db.models import Case, Count, IntegerField, Sum, Value, When
from django.db.models.functions import(
    ExtractYear,
    TruncDay,
    TruncMonth,
    TruncQuarter,
    TruncYear
)

PERIOD_CHOICES = ("daily", "monthly", "quarterly", "semiannual", "yearly")

_TRUNC_FN = {
    "daily": TruncDay,
    "monthly": TruncMonth,
    "quarterly": TruncQuarter,
    "yearly" : TruncYear
}


def annotate_period(queryset, period, date_field = "date"):
    """Group an already-filtered Expense queryset into buckets for `period`
    and return totals ordered chronologically (oldest bucket first).

    period: "daily" | "monthly" | "quarterly" | "semiannual" | "yearly"

    Each row in the result looks like:
      {"bucket": date(...), "total": Decimal(...), "count": int}
    except for "semiannual", which has no Django Trunc* helper, so it
    returns {"year": int, "half": 1|2, "total": Decimal(...), "count": int}
    (half=1 -> Jan-Jun, half=2 -> Jul-Dec).
    """
    
    if period == "semiannual":
        half = Case(
            When(**{f"{date_field}__month__lte": 6}, then = Value(1)),
            default=Value(2),
            output_field=IntegerField(),
        )
        return list(
            queryset.annotate(year=ExtractYear(date_field), half=half)
            .value("year", "half")
            .annotate(total=Sum("amount"), count = Count("id"))
            .order_by("year", "half")
        )
        
    trunc_fn = _TRUNC_FN.get(period)
    if trunc_fn is None:
        raise ValueError(f"Unsupported period '{period}'. Choose one of {PERIOD_CHOICES}.")
    
    return list(
        queryset.annotate(bucket=trunc_fn(date_field))
        .values("bucket")
        .annotate(total=Sum("amount"), count = Count("id"))
        .order_by("bucket")
    )
    

