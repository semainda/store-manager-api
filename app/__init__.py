"""Module that creates the flask app with given env"""
# thirdparty imports
from flask import Flask, Blueprint
from flask_restful import Api
from flask_jwt_extended import JWTManager

# local imports
from instance.config import APP_ENV_CONFIG
from .db_config.store_db_setups import DatabaseOperations

# api endpoints imports
from .api.v2.views.users.login import Login
from .api.v2.views.users.users import Users, UsersActivity, UserProfile
from .api.v2.views.users.roles import Roles, RolesActivity
from .api.v2.views.sales.categories import Categories, CategoriesActivity
from .api.v2.views.sales.sub_categories import SubCategories, SubCategoriesActivity

# blueprint object
API_V2_BLUEPRINT = Blueprint("v1", __name__, url_prefix="/api/v2")
API = Api(API_V2_BLUEPRINT)


class StoreManager:
    """Class that defines the flask app with given config"""

    def __init__(self, config):
        self.app = Flask(__name__, instance_relative_config=True)
        self.app.config.from_object(APP_ENV_CONFIG[config])
        # Create store database table
        self.dt = DatabaseOperations()
        self.dt.create_db_tables(self.app.config["DATABASE_URL"])

        # Create store default admin
        # create_default_admin(self.app.config["DATABASE_URL"])
       
        # blueprint rgistration
        self.app.register_blueprint(API_V2_BLUEPRINT)
        # initialize JWTManager
        JWTManager(self.app)

    def create_app(self):
        """Method that instantiate flask app with a given config"""
        return self.app

######################################################
#           Store Attendants Endpoints               #
######################################################

API.add_resource(Login, "/auth/login")
API.add_resource(UserProfile, "/users/myprofile")

######################################################
#           Store Owner Endpoints                    #
######################################################

API.add_resource(Users, "/users")
API.add_resource(UsersActivity, "/users/<int:user_id>")
API.add_resource(Roles, "/roles")
API.add_resource(RolesActivity, "/roles/<int:role_id>")
API.add_resource(Categories, "/categories")
API.add_resource(CategoriesActivity, "/categories/<int:cat_id>")
API.add_resource(SubCategories, "/subcategories")
API.add_resource(SubCategoriesActivity, "/subcategories/<int:cat_id>")
