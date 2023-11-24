## BAR CHALLENGE BACKEND

You can try the deployed version:
`https://bar-challenge-python.onrender.com/`

To start this project, first run these commands:

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