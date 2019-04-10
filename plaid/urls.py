from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from plaid import views

urlpatterns = [
	path('plaid/account/', views.accounts_list),
	path('plaid/account/<int:pk>/', views.account_detail),
	path('plaid/user/', views.users_list),
	path('plaid/user/<int:pk>/', views.user_detail),
	path('plaid/fetch/', views.call_api)
]

urlpatterns = format_suffix_patterns(urlpatterns)