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
10. Always create an admin user after running the initial migrations


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