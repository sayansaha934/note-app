## API Docs
https://documenter.getpostman.com/view/33036820/2sA2r823uq

## How to setup

  - git clone https://github.com/sayansaha934/note-app.git
  - cd note-app
  - conda create -n venv python==3.8 --y
  - conda activate venv
  - pip install -r requirements.txt
  - Update `noteapp/settings.py`
    ```
    DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "<DB NAME>",
        "USER": "<DB USER>",
        "PASSWORD": "<DB PASSWORD>",
        "HOST": "<DB HOST>",
        "PORT": "<PORT>",
    }
    }
    ```
  - `python manage.py makemigrations`
  - `python manage.py migrate`
  - python manage.py runserver
