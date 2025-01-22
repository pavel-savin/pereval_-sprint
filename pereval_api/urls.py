from django.urls import path
from .views import SubmitDataView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('submitData/', SubmitDataView.as_view(), name='submit-data'),
]

