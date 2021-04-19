# Files of Otters - Ghid rapid

## Instalați Django

```bash
pip install Django==3.2
```

Puteți citi și [aici](https://www.djangoproject.com/download/).

## Pregătiți proiectul local

```bash
python3 manage.py makemigrations # Probabil zice că nu e nimic nou.
python3 manage.py migrate        # Trebuie să arate niște ok-uri.

# Creați un cont administrator - e doar local la voi, dați ce date vreți.
python3 manage.py createsuperuser

# Porniți serverul.
python3 manage.py runserver
```

Intrați în browser la `localhost:8000/filesharing`. Trebuie să vă dea `Hello, world.`.

Puteți accesa și site-ul de administratori la `localhost:8000/admin`.

## Cum lucrăm - branch-uri

Eu zic să facem câte un branch pentru fiecare etapă și să lucrăm pe el. Îi
dăm merge pe `main` abia la finalul etapei. Deci acum vom lucra pe `sprint1`.

Aduceți branch-ul pe local: `git checkout -b sprint1 origin/sprint1`.

Din `sprint1` vom face câte un branch pentru fiecare feature pe care îl scriem,
de exemplu `upload-files`. Când terminăm de implementat feature-ul, dăm pull
request ca să îl aducem în `sprint1`. Dând pull request îi lăsăm și pe ceilalți
coechipieri să dea review înainte să modificăm permanent.

## Linkuri

[Tutorial Django (destul de lung)](
https://docs.djangoproject.com/en/3.2/intro/tutorial01/).
