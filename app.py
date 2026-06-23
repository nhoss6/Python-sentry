import os

import sentry_sdk
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from sentry_sdk.integrations.flask import FlaskIntegration

from product_repository import (
    create_product,
    delete_product,
    get_all_products,
    get_product_by_id,
    update_product,
)


load_dotenv()

sentry_dsn = os.getenv("SENTRY_DSN")
if sentry_dsn:
    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[FlaskIntegration()],
        environment=os.getenv("ENVIRONMENT", "development"),
        release=os.getenv("APP_RELEASE", "api-python-mysql-swagger@1.0.0"),
        send_default_pii=False,
        traces_sample_rate=float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", "0.0")),
    )


app = Flask(__name__)
CORS(app)

api = Api(
    app,
    version="1.0",
    title="API Produits",
    description="API Python Flask connectee a MySQL/phpMyAdmin avec Swagger",
    doc="/swagger",
)

product_namespace = api.namespace(
    "products",
    description="Gestion des produits",
)

product_model = api.model("Product", {
    "nom": fields.String(required=True, description="Nom du produit", example="Clavier"),
    "prix": fields.Float(required=True, description="Prix du produit", example=49.99),
    "stock": fields.Integer(required=True, description="Stock disponible", example=10),
})

product_response_model = api.model("ProductResponse", {
    "id": fields.Integer(description="Identifiant du produit", example=1),
    "nom": fields.String(description="Nom du produit", example="Clavier"),
    "prix": fields.Float(description="Prix du produit", example=49.99),
    "stock": fields.Integer(description="Stock disponible", example=10),
})


@api.route("/")
class Home(Resource):
    def get(self):
        return {
            "message": "API Python connectee a MySQL avec Swagger"
        }


@product_namespace.route("")
class ProductList(Resource):

    @product_namespace.marshal_list_with(product_response_model)
    def get(self):
        return get_all_products()

    @product_namespace.expect(product_model)
    def post(self):
        data = api.payload

        nom = data.get("nom")
        prix = data.get("prix")
        stock = data.get("stock")

        if not nom or prix is None or stock is None:
            return {
                "error": "nom, prix et stock sont obligatoires"
            }, 400

        new_id = create_product(nom, prix, stock)

        return {
            "message": "Produit cree",
            "id": new_id
        }, 201


@product_namespace.route("/<int:product_id>")
class ProductItem(Resource):

    @product_namespace.marshal_with(product_response_model)
    def get(self, product_id):
        produit = get_product_by_id(product_id)

        if produit is None:
            api.abort(404, "Produit introuvable")

        return produit

    @product_namespace.expect(product_model)
    def put(self, product_id):
        data = api.payload

        nom = data.get("nom")
        prix = data.get("prix")
        stock = data.get("stock")

        if not nom or prix is None or stock is None:
            return {
                "error": "nom, prix et stock sont obligatoires"
            }, 400

        lignes_modifiees = update_product(product_id, nom, prix, stock)

        if lignes_modifiees == 0:
            api.abort(404, "Produit introuvable")

        return {
            "message": "Produit modifie"
        }

    def delete(self, product_id):
        lignes_supprimees = delete_product(product_id)

        if lignes_supprimees == 0:
            api.abort(404, "Produit introuvable")

        return {
            "message": "Produit supprime"
        }


@app.route("/debug-sentry")
def trigger_error():
    if os.getenv("ENVIRONMENT", "development") != "development":
        return {
            "error": "Route de demonstration desactivee hors environnement development"
        }, 403

    raise RuntimeError("Erreur volontaire pour demonstration Sentry + GitHub Issues")


if __name__ == "__main__":
    app.run(debug=True)
