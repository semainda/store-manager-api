from flask import Flask, Blueprint
from flask_restful import Api
from .login import Login
from .users import Users, UsersActivity, UserProfile
from .roles import Roles, RolesActivity
from .users_roles import UserRoles, UserRolesActivity, UserRoleActivity

users_blueprint = Blueprint("users", __name__, url_prefix="/api/v2")
api = Api(users_blueprint)
api.add_resource(Login, "/auth/login")
api.add_resource(UserProfile, "/users/profile")
api.add_resource(Users, "/users")
api.add_resource(UsersActivity, "/users/<int:user_id>")
api.add_resource(Roles, "/roles")
api.add_resource(RolesActivity, "/roles/<int:role_id>")
# works for all users with given role_id
api.add_resource(UserRoles, "/users/roles")
api.add_resource(UserRolesActivity, "/users/roles/<int:role_id>")
# works for specific user with given user_role_id
api.add_resource(UserRoleActivity, "/users/roles/user/<int:user_role_id>")