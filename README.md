## BAR CHALLENGE BACKEND

You can try the deployed version:
`https://bar-challenge-python.onrender.com/`

To start this project, ensure that you have a folder that would contain all projects.

first run these commands:

(In case you dont have a virtual environment) Install a new virtual environment:

```bash
python -m virtualenv venv
```

Start your virtual environment:

```bash
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```
After that, install packages:

```bash
pip install -r requirements.txt
```

Run the migrations:
```bash
python manage.py migrate
```

And start the project:
```bash
python manage.py runserver
```