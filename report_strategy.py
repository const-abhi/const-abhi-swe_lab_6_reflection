"""Strategy pattern: interchangeable report aggregation algorithms."""
from abc import ABC, abstractmethod


class ReportStrategy(ABC):
    @abstractmethod
    def generate(self, expenses):
        raise NotImplementedError


class MonthlyReportStrategy(ReportStrategy):
    def generate(self, expenses):
        totals = {}
        for row in expenses:
            month = row[3][:7]  # YYYY-MM from expense date
            totals[month] = totals.get(month, 0.0) + float(row[1])
        return dict(sorted(totals.items()))


class CategoryReportStrategy(ReportStrategy):
    def generate(self, expenses):
        totals = {}
        for row in expenses:
            category = row[2]
            totals[category] = totals.get(category, 0.0) + float(row[1])
        return dict(sorted(totals.items()))
