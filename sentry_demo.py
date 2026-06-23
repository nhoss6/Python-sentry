"""
================================================
DEMO - Cours Ticketing : Sentry + GitHub Issues
================================================

Objectif :
1. Initialiser Sentry avec une variable d'environnement.
2. Provoquer une erreur volontaire.
3. Verifier l'erreur dans Sentry.
4. Creer une GitHub Issue depuis Sentry.

Important :
Le DSN Sentry ne doit jamais etre ecrit dans le code.
Il doit etre fourni via la variable d'environnement SENTRY_DSN.
"""

import os

import sentry_sdk
from dotenv import load_dotenv


load_dotenv()

sentry_dsn = os.getenv("SENTRY_DSN")

if not sentry_dsn:
    print("SENTRY_DSN est manquant.")
    print("Creez un fichier .env local ou exportez la variable d'environnement.")
    raise SystemExit(1)

sentry_sdk.init(
    dsn=sentry_dsn,
    traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
    release=os.getenv("APP_RELEASE", "api-python-mysql-swagger@1.0.0"),
    environment=os.getenv("ENVIRONMENT", "development"),
    send_default_pii=False,
)

print("Sentry initialise avec succes.")
print("=" * 50)


def get_user_by_id(user_id):
    """Simule une requete base de donnees pour trouver un utilisateur."""
    users_db = {
        1: {"nom": "Alice", "email": "alice@example.com"},
        2: {"nom": "Bob", "email": "bob@example.com"},
    }

    # Erreur volontaire : si user_id=99, la cle n'existe pas.
    return users_db[user_id]


sentry_sdk.set_tag("cours", "ticketing_sentry_github")
sentry_sdk.set_tag("demo", "erreur_volontaire")

print("Tentative d'acces a l'utilisateur ID=99 (inexistant)...")
print("=" * 50)

try:
    utilisateur = get_user_by_id(99)
    print(f"Utilisateur trouve : {utilisateur}")
except KeyError as erreur:
    print(f"Erreur capturee : utilisateur {erreur} introuvable.")

    sentry_sdk.set_context("demo", {
        "user_id_recherche": 99,
        "message": "L'utilisateur demande n'existe pas en base de donnees",
    })
    sentry_sdk.capture_exception(erreur)
    print("Erreur envoyee a Sentry.")

print("=" * 50)
print("Verifiez maintenant votre dashboard Sentry, puis creez une GitHub Issue.")
