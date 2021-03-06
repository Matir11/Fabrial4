# Django Secret Key Secured

## Resources:

* https://github.com/PdxCodeGuild/class_otter/blob/main/5%20Capstone/Heroku%20Deployment.md#environment-variables

### Create `SECRET_KEY`:  
```
> python .\manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

## Relevent commit:
* https://github.com/brucestull/DjangoCustomUserStarter/commit/609a3714d59340d30fa55ff5022f830bebd1b3bd

## Process:

1. Modify `fabrial_proj/settings.py`:  
    ```
    import os

    SECRET_KEY = os.environ.get('SECRET_KEY')
    ```

1. Create new `SECRET_KEY`:  
    ```
    > python .\manage.py shell
    >>> from django.core.management.utils import get_random_secret_key
    >>> print(get_random_secret_key())
    ```

1. Add new `SECRET_KEY` to environment variables in production.

1. Push changes to Heroku:  
`git push heroku main`

1. Test deployed application:  
    * Use your link to your Heroku deployment. The next link is to my Heroku deployment of this custom user repo.
    * https://django-custom-user-starter.herokuapp.com/
