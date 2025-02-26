from django.http import HttpResponse
import csv

def export_expenses_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="expenses.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Amount'])

    # Example data (replace this with actual database query)
    expenses = [
        ['2024-02-26', 'Food', '100'],
        ['2024-02-25', 'Transport', '50'],
    ]

    for expense in expenses:
        writer.writerow(expense)

    return response

def export_expenses_pdf(request):
    return HttpResponse("PDF export feature coming soon.")

def check_budget(request):
    return HttpResponse("Budget check feature coming soon.")

