from django.urls    import path

from users.views    import check_existing_username, check_existing_email, SignUpView, SignInView

urlpatterns = [
    path('/username', check_existing_username), 
    path('/email', check_existing_email),
    path('/signup', SignUpView.as_view()),
    path('/signin', SignInView.as_view())
]