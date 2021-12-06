from django.urls    import path

from users.views    import check_existing_username, check_existing_email, SignUpView

urlpatterns = [
    path('/username', check_existing_username), 
    path('/email', check_existing_email),
    path('/signup', SignUpView.as_view()), 
]