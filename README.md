# Mini Library Management System

<font size=5>**Check out [Reproduction Guide](./IdeasAndReproduction.md) for more details**</font>

Simple and Robust Django Rest Framework(DRF) library system.

# What one can do with it
+ View available books
+ Make borrowings(upto limits)
+ Return books
+ Extend the return date of books
+ Read API specifications using Swagger UI

# What one cannot expect from it
+ Not a full fledged full stack application with support for frontend interaction, this is an API
+ Though the admin panel supports adding books and their copies, this is not an library inventory management system.

# Requirements(Recommended)
+ [uv](https://docs.astral.sh/uv/getting-started/installation/)

# Guide to install


```bash
git clone https://github.com/pseudoClone/minlibsys.git
```

```bash
cd minlibsys
```

+ Create the virtual environment:
```bash
uv sync
```

+ Run the migrations for DB(SqLite3):

```bash
uv run manage.py makemigrations
uv run manage.py migrate
```

+ To work with the admin panel and create books and authors, make a superuser
```bash
uv run manage.py createsuperuser
```