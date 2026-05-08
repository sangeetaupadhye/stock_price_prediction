from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('upload/', views.upload_dataset, name='upload'),
    path('predict/', views.predict_view, name='predict'),
    # path('predict-page/', views.predict_page, name='predict_page'),
    path('charts/', views.charts_page, name='charts'),
    path('chart-data/', views.chart_data, name='chart_data'),
    path('info/', views.info_page, name='info'),  

]