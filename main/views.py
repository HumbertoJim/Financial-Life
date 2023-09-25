from django.shortcuts import render

from records.models import Record
from django.db.models import Sum, F, ExpressionWrapper, DecimalField, Case, When

def home(request):
    if request.user.is_authenticated:
        # Consulta para obtener los datos agrupados por fecha y categoria
        data = Record.objects.filter(user=request.user).values('datetime', 'category__name').annotate(
            total_value=ExpressionWrapper(
                Sum(F('value') * Case(When(is_income=True, then=1), default=-1, output_field=DecimalField())),
                output_field=DecimalField()
            )
        )

        # Estructura de datos para almacenar los datos en un formato adecuado para graficar
        chart_data = {}

        for entry in data:
            category_name = entry['category__name']
            if category_name not in chart_data:
                chart_data[category_name] = []

            chart_data[category_name].append((entry['datetime'], entry['total_value']))
        context = {'chart_data': chart_data}
    else:
        context = {}
    print(context)
    return render(request, 'home.html', context)