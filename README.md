# Files of Otters - Ghid rapid

## Copiați credențialele de pe Whatsapp

Trebuie să copiați fișierul la calea `~/.aws/credentials`.
Creați voi folderul `.aws` dacă nu există.

## Instalați Django și alte biblioteci

```bash
pip install -r requirements.txt
```

## Pregătiți proiectul local

```bash
# Configurați baza de date locală - trebuie să arate niște ok-uri.
python3 manage.py migrate

# Creați un cont administrator - e doar local la voi, dați ce date vreți.
python3 manage.py createsuperuser

# Porniți serverul.
python3 manage.py runserver
```

Intrați în browser la `localhost:8000/filesharing`. Trebuie să vă redirecționeze
la o pagină de logare.

Puteți crea un cont nou la `localhost:8000/filesharing/register`.

Puteți accesa și site-ul de administratori la `localhost:8000/admin`.

## Cum lucrăm - branch-uri

Eu zic să facem câte un branch pentru fiecare etapă și să lucrăm pe el. Îi
dăm merge pe `main` abia la finalul etapei. Deci acum vom lucra pe `sprint3`.

Aduceți branch-ul pe local: `git checkout -b sprint3 origin/sprint3`.

Din `sprint3` vom face câte un branch pentru fiecare feature pe care îl scriem,
de exemplu `tag-buttons`. Când terminăm de implementat feature-ul, dăm pull
request ca să îl aducem în `sprint3`. Dând pull request îi lăsăm și pe ceilalți
coechipieri să dea review înainte să modificăm permanent.

## Linkuri

[Tutorial Django (citește-l)](
https://docs.djangoproject.com/en/3.2/intro/tutorial01/).
