# Demo Sentry + GitHub Issues avec Flask

Ce depot sert de support de cours pour montrer le cycle complet :

1. une API Flask provoque une erreur volontaire ;
2. Sentry capture l'erreur ;
3. l'erreur est transformee en GitHub Issue ;
4. la correction peut ensuite etre suivie via GitHub.

## Regle de securite importante

Le DSN Sentry ne doit jamais etre ecrit dans le code.

Le code lit uniquement la variable d'environnement `SENTRY_DSN`.

## Installation

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Configuration locale

Copier le fichier d'exemple :

```powershell
copy .env.example .env
```

Puis remplir localement :

```env
SENTRY_DSN=votre_dsn_sentry
ENVIRONMENT=development
APP_RELEASE=api-python-mysql-swagger@1.0.0
SENTRY_TRACES_SAMPLE_RATE=0.0
```

Le fichier `.env` est ignore par Git.

## Lancer l'API Flask

```powershell
python app.py
```

Swagger :

```txt
http://127.0.0.1:5000/swagger
```

Route de test Sentry :

```txt
http://127.0.0.1:5000/debug-sentry
```

Cette route leve volontairement une exception pour l'envoyer a Sentry.

## Script autonome de demo

```powershell
python sentry_demo.py
```

Ce script provoque une erreur `KeyError` volontaire et l'envoie a Sentry.

## Workflow pedagogique

1. Ouvrir Sentry.
2. Verifier que l'erreur apparait dans le projet.
3. Ouvrir le detail de l'erreur.
4. Cliquer sur `Create GitHub Issue`.
5. Choisir le depot `nhoss6/Python-sentry`.
6. Creer l'issue.
7. Corriger le code dans une branche.
8. Ouvrir une pull request.

## Routes API

```txt
GET     /
GET     /products
POST    /products
GET     /products/{product_id}
PUT     /products/{product_id}
DELETE  /products/{product_id}
GET     /debug-sentry
```
