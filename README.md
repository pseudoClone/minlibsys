# Mini Library Management System

<font size=5>**Check out [Reproduction Guide](./IdeasAndReproduction.md) for more details**</font>

Simple and Robust Django Rest Framework(DRF) library system.

# What one can do with it
+ View available books
+ Make borrowings(upto limits)
+ Return books(on time)
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
## Docker version
To run the docker version, ensure that the new docker-buildx package is in the system.
`sudo pacman -S docker-buildx` or the relevant package install command of the distro repository
1. `docker buildx build -t minlibsysimage .`
2. `docker run -p 8000:8000 --name minlibsyscontainer minlibsysimage`


# Limitations
1. Should have used PostgreSQL but that would mean separate server and I would need to package the application and DB server, both with Docker. While that could be done because of my work with Docker and Podman earlier, making a strong API system is priority here.
2. Never done unit tests automatically before , and, it's still new to me, hence, it will take time to test all of the different systems such as auth, querying system, Django exceptions(because DRF exceptions are non existent), and borrowing edge cases.