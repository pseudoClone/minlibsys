# Steps to reproduce

## Tools Used
1. ruff by Astral
2. uv again by Astral

## Setup
1. `uv init` to initialize the project
2. `uv sync` because for some reason, VSCode didn't install the dependencies automatically
3. `uv add django djangorestframework` to add the dependencies
4. `uv run django-admin startproject minsyslib .` because I don't want a separate project folder
5. `uv run manage.py runserver` to check if I actually did the setup correct and application should be starting on the right port
6. Write models for each application
7. I accidentally created separate commits for separate apps. That's redundant. So, squashing it. `git rebase -i HEAD ~7` and put `s` in the commits you want to squash to one.
8. Add your apps to `settings.py` before making migrations.
9. Run `uv run manage.py makemigrations` followed by `uv run manage.py migrate`
10. Always create an admin user after running the initial migrations `python manage.py createsuperuser`
11. Since, admin panel is not configured with the model with `ModelAdmin`, I won't touch it for now.


## Code organization

1.  ```zsh
        uv run django-admin startapp book
        uv run django-admin startapp member
        uv run django-admin startapp author
        uv run django-admin startapp borrowing


### Books Model
+ Since ISBN is only numbers followed by dashes. There is no point allowing characters of any kind other than numbers and dashes.
+ [This site](https://regex101.com/) has support for building Python style regex. So, since I don't know regex, `r"[0-9-]"`(remembering from using `sed` from 2 years ago) is what I tested and it worked.
+ But `re` and `Regex` would not match with `validators=` argument in `model.CharField`. Hence, a quick [Google lookup](https://www.google.com/search?q=regex+validation+django+models) showed that I could use `django.core.validators.RegexValidator`.
+ Update: Regex fails miserably because validation sucks. Mainly because I didn't know that ISBN-10 can contain an X in the last place. So, I tried: `r"[0-9X]"` but that allows X to appear anywhere and also in ISBN-13. So, I have to update my regex. Also, the regexx`r"[0-9-]"` sucks because I have already restricted usage of `-` in the model. So, going back to ISBN-10. So, this has to be right. `^(?:\d{9}[\dX]|\d{13})$`.
+ The code for ISBN validation came from [this page](https://www.instructables.com/How-to-verify-a-ISBN/)

### Borrowing Model
+ We create a many to one relation from borrowing to member since one member can borrow many books.
+ A major flaw here is the since we have `book_copy` that can be borrowed, the same book can be borrowed multiple times.
+ Here, from my time working with SQL for an interview, I remember that indices are ordered. And by adding the constraint, I am enforcing that using the unique index, `book_copy.id` must be unique for all the rows where `book_copy.id == NULL`.
+ So the work of the index is that we are creating it in the `book_copy`. So, every `id` of book_copy gets a unique index, but if the `returned_at` is `NULL` i.e if the book has not been returned, we cannot create a new index on it or in business logic, we cannot create a new entry for it's borrowing.
+ The models.Q is a `Q Object` which I searched from that helps me to set condition for enforcing uniqueness. I didn't know this. Hence, [Google](https://www.google.com/search?q=how+to+enforce+uniqueness+of+a+row+in+django&sca_esv=17108f0ef32378c7&ei=AqpYarfzD-WWwcsP4d2e2A8&biw=1495&bih=775&ved=0ahUKEwi3_IPB9taVAxVlS3ADHeGuB_sQ4dUDCBI&uact=5&oq=how+to+enforce+uniqueness+of+a+row+in+django).

### Borrowing Logic
+ So, the first headache is renewal, and while `expected_return_at` and `borrowed_at` are both editable, it wouldn't be nice to extend it or edit it. Instead, renewal should be, press a button or activate a flag and we set it to returned and make a new transaction. But then again, how many times a person can renew? Can he/she hog the book by renewing it endlessly? Nope. So, there must be a renewing logic. I am still conflicted as to if I make this a logic based feature or model constraint based framework using window functions of SQL.
+ For now, Google AI told me to use renewal_count model for this problem, to check how many renews are done and using services to track the state.
+ So, for this I will use services, name derived from [NestJS Services](https://github.com/pseudoClone/lynxBackend/blob/main/src/links/links.service.ts), Controllers and Modules, somehow common in Django too.
+ We don't need to refresh the latest state of DB in Django ORM unlike **Prisma** or **Drizzle**. Because Django automatically pull the latest state.
+ To not throw fatal exceptions, Django gives this really cool feature called [subtransaction](https://docs.djangoproject.com/en/6.0/topics/db/transactions/#:~:text=Wrapping%20atomic%20in%20a%20try/except%20block%20allows%20for%20natural%20handling%20of%20integrity%20errors%3A) And this allows me to handle exceptions without fatal errors. 
+ So some complex queries cannot be handled with ad-hoc queries. Hence for some models, we need to have custom querysets and they can be paired with custom query set managers as explained [here](https://medium.com/@sohampanchal1469/unlocking-the-power-of-django-managers-customizing-querysets-and-model-methods-0ffaae7bd40f#:~:text=class%20PublishedManager(models.Manager)%3A%0A%20%20%20%20def%20get_queryset(self)%3A%0A%20%20%20%20%20%20%20%20return%20PublishedQuerySet(self.model%2C%20using%3Dself._db))


### Admin Panel

+ I love admin panel because this comes right after creating my favourite part i.e creating models. And for this, the idea is simple. We create admin panel to sift through different books and members and stuff.
+ So, I create admin classes for everything with filter and search fields for relevant stuff
+ Also, I love this cool decorator method called display that let's me alter anything on the admin page. And it helps me join the names in Author Admin
+ Could be fun if it used fuzzy search. But not really sure if it uses fuzzy search.


### Serializers
+ DRF has serializers which are literally what the name says, serializers for different things in the app like requests and models. Protobuf, JSON, XML are all serialization formats and this is the first time I have had to work with this serious serialization configuration.
+ So, first, I make DRF serializers. And only then routes and stuff. And finally OpenAPI integration. Might(Big might) even see, SwaggerUI like the way FastAPI does


### Testing
+ Until now, I have never done testing wiht DRF or with Django. So, this is new. So, as per the [docs](https://docs.djangoproject.com/en/6.0/topics/testing/overview/#:~:text=from%20django.test%20import,cat%20says%20%22meow%22%27), and actually I can see it too, that every app has it's own test files and the project wide testing can be created with a tests directory. I will take the first approach for unit testing. E2E testing is beyond the scope of this project.
+ For now, I only check if 2 people or more can borrow the same book and nothing more. Manually adding books and member can be automated but that would mean that has to be dependency injection which Django does not support. Until then, I will do it manually. I love FastAPI and Nest.js because of this.


### OpenAPI compatibility

+ A quick [search](https://www.google.com/search?q=drf+spectacular+vs+drf+yasg) tells me that I should use drf-spectacular for generating API docs.
+ I don't know how to do this plumbing because I expect it to work like it does with FastAPI but still I will install it as the [docs say](https://drf-spectacular.readthedocs.io/en/latest/readme.html#requirements:~:text=3.15%2C%203.16%2C%203.17-,Installation,-%C2%B6).
+ Almost everything should be out-of-the-box plug and play for this but I still have to update some project wide settings and urls for api docs.

### Viewset protection
+ For viewset protection, we can just use DRF `IsAuthenticated`
+ But this goes way back to authetication using a scalable method, like that one time I used [Django-allauth](https://github.com/pseudoClone/profile-dashboard)


### Features
+ For now, this has the basics but one thing that is needed is fine accumulation which is another story because I am thinking of cron jobs to auto increase the fine as the days pass for a user when he/she has not returned the book past their expected and scalable secure authentication because while we ask the user for e-mail, it is not a required field. And the authentication is done from the `AbstractUser` class using the username.
+ The issues with email is that, while I can use the `Django Validator` for validating the email string, there is no simple way to check if the email is valid. And having used temporary emails to sign-up for services, my hypocricy does not let me setup a simple email validator. This needs a proper setup.
+ But then again I searched for [temp email sign up detection Django](https://www.google.com/search?sxsrf=APpeQnusDQoVaKkfoghwS_8NZ4kaFMDUBA:1784437331048&udm=web&q=temporary+email+sign+up+detection+Django) and subsequently led me to [this repo](https://github.com/disposable-email-domains/disposable-email-domains)
+ But then I thought again, why bother with email, because while email can be used to authenticate user, I am not gonna use something like mailgun to send emails to people asking them to verify their email. THat would be too much for the scope of the project. So, I am defaulting to username. [Resend](https://resend.com/) is another alternative but the argument remains the same. Hence, **USERNAME** it is. 


### User Registration
+ Okay so, generics to automate the post method here so that i don't have to write methods with decorators for path and stuff. [Here it says ](https://www.django-rest-framework.org/api-guide/generic-views/#createapiview:~:text=rest_framework.generics.-,CreateAPIView,Provides%20a%20post%20method%20handler.,-Extends%3A%20GenericAPIView)that it provides me with a generic post method. 
+ In the code, the AllowAny permission guard is for the fact, that anyone should be able to create accounts, and not like other protected methods where I restricted them to allow only the authenticated users.
+ [This page](https://pavansaibolliboina.medium.com/django-rest-framework-generics-91d3d095baa2#:~:text=from%20rest_framework.generics%20import%20CreateAPIView%0Afrom%20.models%20import%20Book%0Afrom%20.serializers%20import%20BookSerializer%0A%0Aclass%20BookCreateAPIView(CreateAPIView)%3A%0A%20%20%20%20queryset%20%3D%20Book.objects.all()%0A%20%20%20%20serializer_class%20%3D%20BookSerializer) was a godsend for generics
+ Finally like before we have to create API routes for signing up members/users. And that means, I need to go back to global [urls file](./minlibsys/urls.py)