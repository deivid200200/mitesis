from django.urls import path
from . import views

app_name = 'reportes'

urlpatterns = [
    path('expediente/<int:estudiante_id>/pdf/', views.GenerarExpedientePDFView.as_view(), name='expediente_pdf'),
    path('acta-culminacion/<int:acta_id>/pdf/', views.GenerarActaCulminacionPDFView.as_view(), name='acta_culminacion_pdf'),
    path('notas/<int:estudiante_id>/excel/', views.GenerarActaNotasExcelView.as_view(), name='notas_excel'),
]
