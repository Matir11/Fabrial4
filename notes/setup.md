# Django Custom User Starter Notes

## NOTE:
* This documents uses '\\' as directory delimiter. Users of other operating systems may need to use '/' as their directory delimiter.

### Set up Virtual Environment

1. It is assumed pipenv has already been installed. One way is `pip install pipenv`.

1. Ensure your terminal session is within the root of project. Usually same directory as `manage.py`.

1. Create pipenv and install Django, Docutils and any other packages needed. Packages can be installed later with similar `pipenv install` command:  
    `pipenv install django==3.2 docutils==0.18.1`

1. Note virtual environment location and starting command:
    * Virtual Environment activation:
        * Powershell:  
        `C:\<path to virtual environment>\Scripts\activate.ps1`
        * BASH:  
        `source C:/<path to virtual environment>/Scripts/activate`

1. Activate virtual environment (Once python interpreter is chosen in VS Code, this command might not be needed):  
    `C:\<path to virtual environment>\Scripts\activate.ps1`

### Set up Django:

1. Create project skeleton:  
    `django-admin startproject fabrial_proj .`

1. Create `users` app:  
    `python manage.py startapp users`

1. Test for green rocket:  
    * Start server at some port (I have chosen optional non-default 8010):  
    `python manage.py runserver 8010`
    * Verify green rocket:  
    `http://localhost:8010/`

1. Stop the server:  
    * Ctrl + c

1. Modify `fabrial_proj\settings.py`:
    ```
    INSTALLED_APPS = [
        ...
        'users.apps.UsersConfig', # Our addition from users.apps.UsersConfig
        ...
    ]

    AUTH_USER_MODEL = "users.CustomUser"    # Our addition
    ```

1. Modify `users\models.py`:
    * Our `CustomUser` which inherits `AbstractUser` has lots of functionality already built in. See some other documentation for info.
    ```
    from django.contrib.auth.models import AbstractUser

    class CustomUser(AbstractUser):
        pass
        # add additional fields in here

        def __str__(self):
            return self.username
    ```

1. Create `users\forms.py`:
    ```
    from django.contrib.auth.forms import UserCreationForm, UserChangeForm

    from .models import CustomUser

    class CustomUserCreationForm(UserCreationForm):

        class Meta:
            model = CustomUser
            fields = ("username", "email")

    class CustomUserChangeForm(UserChangeForm):

        class Meta:
            model = CustomUser
            fields = ("username", "email")
    ```

1. Modify `users\admin.py`:
    ```
    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin

    from .forms import CustomUserCreationForm, CustomUserChangeForm
    from .models import CustomUser

    class CustomUserAdmin(UserAdmin):
        add_form = CustomUserCreationForm
        form = CustomUserChangeForm
        model = CustomUser
        list_display = ["email", "username",]

    admin.site.register(CustomUser, CustomUserAdmin)
    ```

1. Create migrations for `users` app:  
    `python manage.py makemigrations users`

1. View the migrations which will be applied to `users` app:  
    * Get current migration number from `users\migrations`:  
    `ls .\users\migrations\`  
    * Sample output:  
        ```
        Mode                 LastWriteTime         Length Name
        ----                 -------------         ------ ----
        -a---           5/20/2022 12:20 PM           2921 0001_initial.py
        ```
    * We use `0001`, in this case, since `0001` is the prefix of the most recent migration `0001_initial.py`:  
    `python manage.py sqlmigrate users 0001`  
    * Sample output:
    ```

    ```

1. Apply the migrations to `users` app:  
    `python manage.py migrate`

1. Create `superuser`:  
    `python manage.py createsuperuser`

1. Modify `fabrial_proj\settings.py`:  
    * Direct Django templates engine to appropriate directory (in 'TEMPLATES' section).
        ```
        TEMPLATES = [
            {
                ...
                'DIRS': [BASE_DIR / "templates"],   # Our change
                ...
            },
        ]
        ```
    * Set login and logout redirects (at bottom of file):
        ```
        LOGIN_REDIRECT_URL = "home"     # Our addition
        LOGOUT_REDIRECT_URL = "home"    # Our addition
        ```

1. Create directories and files:  
    * Directories:  
        `fabrial_proj\templates`  
        `fabrial_proj\templates\registration`  
    * Files:  
        `fabrial_proj\templates\base.html`  
        `fabrial_proj\templates\home.html`  
        `fabrial_proj\templates\registration\login.html`  
        `fabrial_proj\templates\registration\signup.html`  

1. Add contents to `fabrial_proj\templates\base.html`:
    ```
    <!DOCTYPE html>
    <html>
        <head>
            <meta charset="utf-8">
            <title>{% block title %}Django Auth Tutorial{% endblock %}</title>
        </head>
        <body>
            <main>
                {% block content %}
                {% endblock %}
            </main>
        </body>
    </html>
    ```

1. Add contents to `fabrial_proj\templates\home.html`:
    ```
    {% extends "base.html" %}

    {% block title %}Home{% endblock %}

    {% block content %}
        {% if user.is_authenticated %}
            Hi {{ user.username }}!
            <p><a href="{% url 'logout' %}">Log Out</a></p>
        {% else %}
            <p>You are not logged in</p>
            <a href="{% url 'login' %}">Log In</a> |
            <a href="{% url 'signup' %}">Sign Up</a>
        {% endif %}
    {% endblock %}
    ```

1. Add contents to `fabrial_proj\templates\registration\login.html`:
    ```
    {% extends "base.html" %}

    {% block title %}Log In{% endblock %}

    {% block content %}
        <h2>Log In</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Log In</button>
        </form>
    {% endblock %}
    ```

1. Add contents to `fabrial_proj\templates\registration\signup.html`:
    ```
    {% extends "base.html" %}

    {% block title %}Sign Up{% endblock %}

    {% block content %}
        <h2>Sign Up</h2>
        <form method="post">
            {% csrf_token %}
            {{ form.as_p }}
            <button type="submit">Sign Up</button>
        </form>
    {% endblock %}
    ```

1. Modify `fabrial_proj\urls.py` to match something similar:
    ```
    from django.contrib import admin
    from django.urls import path, include
    from django.views.generic.base import TemplateView

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('users/', include('users.urls')),
        path('users/', include('django.contrib.auth.urls')),
        path('', TemplateView.as_view(template_name='home.html'), name='home'),
    ]
    ```

1. Create `users\urls.py`:
    ```
    from django.urls import path

    from .views import SignUpView

    urlpatterns = [
        path("signup/", SignUpView.as_view(), name="signup"),
    ]
    ```

1. Modify `users\views.py`:
    ```
    from django.urls import reverse_lazy
    from django.views.generic.edit import CreateView

    from .forms import CustomUserCreationForm

    class SignUpView(CreateView):
        form_class = CustomUserCreationForm
        success_url = reverse_lazy('login')
        template_name = 'registration/signup.html'
    ```

1. Test user login/logout/signup:  
    `python manage.py runserver 8010`

1. Test admin interface:  
    * `http://localhost:8010/admin/`

## Set up docutils:  
1. Modify `fabrial_proj\settings.py`:
    ```
    INSTALLED_APPS = [
        ...
        'django.contrib.admindocs',
        ...
    ]
    ```

1. Modify `fabrial_proj\urls.py` (insert before 'admin/' entry):
    ```
    urlpatterns = [
        ...
        path('admin/doc/', include('django.contrib.admindocs.urls'))
        ...
    ]
    ```

