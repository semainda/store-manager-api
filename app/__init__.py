"""Module that creates the flask app with given env"""
# thirdparty imports
from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

# local imports
from instance.config import APP_ENV_CONFIG
from .db_config.db_setups import DataStuctures

# api endpoints imports
from .api.v1.views.users.login import Login
from .api.v1.views.users.users import Users, UsersActivity, UserProfile
from .api.v1.views.users.roles import Roles, RolesActivity
from .api.v1.views.users.users_roles import UserRoles, UserRolesActivity
from .api.v1.views.sales.categories import Categories, CategoriesActivity
from .api.v1.views.sales.products import Products, ProductsActivity
from .api.v1.views.sales.sales import Sales, SalesActivity
from .api.v1.views.sales.sales_summary import SalesSummary,\
SalesSummaryActivity, UserSalesSummary

# blueprint object
API_V1_BLUEPRINT = Blueprint("v1", __name__, url_prefix="/api/v1")
API = Api(API_V1_BLUEPRINT)


class StoreManager:
    """Class that defines the flask app with given config"""

    def __init__(self, config):
        self.app = Flask(__name__, instance_relative_config=True)
        self.app.config.from_object(APP_ENV_CONFIG[config])
         # Create store data stuctures and default administrator
        self.dt_tb = DataStuctures()
        self.dt_tb.init_db()
        self.owner = self.dt_tb.create_default_admin(
            self.app.config["DEFAULT_ADMIN"])
        print(self.owner)
        # blueprint rgistration
        self.app.register_blueprint(API_V1_BLUEPRINT)
        # initialize JWTManager
        JWTManager(self.app)

    def create_app(self):
        """Method that instantiate flask app with a given config"""
        return self.app

######################################################
#           Store Attendants Endpoints               #
######################################################

API.add_resource(Login, "/auth/login")
API.add_resource(Products, "/products")
API.add_resource(ProductsActivity, "/products/<int:prod_id>")
API.add_resource(Sales, "/sales")
API.add_resource(SalesActivity, "/sales/<int:sale_id>")
API.add_resource(SalesSummaryActivity, "/sales/mysales")
API.add_resource(UserProfile, "/users/myprofile")

######################################################
#           Store Owner Endpoints                    #
######################################################

API.add_resource(Roles, "/roles")
API.add_resource(RolesActivity, "/roles/<int:role_id>")
API.add_resource(Users, "/users")
API.add_resource(UsersActivity, "/users/<int:user_id>")
API.add_resource(UserRoles, "/users/roles")
API.add_resource(UserRolesActivity, "/users/roles/<int:user_role_id>")
API.add_resource(SalesSummary, "/sales/summary")
API.add_resource(UserSalesSummary, "/sales/summary/<int:user_id>")
API.add_resource(Categories, "/categories")
API.add_resource(CategoriesActivity, "/categories/<int:cat_id>")
