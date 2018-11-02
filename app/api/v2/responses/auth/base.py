"""Module that handels general auth responses"""


class AuthResponses:
    """Class that handels general Auth responses"""
    def forbidden_user_access_response(self):
        """Method that returns unauthorized response"""
        return {
            "Message":
            "Your not authorized to access this resource. "
            "Make sure you have assigned the required role "
            "to access this resource"
            }, 403

    def unauthorized_user_access_responses(self):
        """Method that returns logged in response """
        return {
            "Message": "You should login first to access this resource"
            }, 401

    def user_login_with_error_response(self):
        """Method that returns incorrect login"""
        return {"Message": "Invalid username/password supplied"}, 401

    def user_success_login_response(self, user_name, access_token):
        """Method that returns valid login response"""
        return {
            "Message":
            "Holaa! You Logged in as {}.".format(user_name),
            "Token": "{}".format(access_token)}, 201
    
    def forbidden_user_role_delete_response(self):
        """Method that returns unauthorized delete response"""
        return {
            "Message": 
            "This role has already being assigned to users."
            "To delete it, revoke it from users first"}, 403
    
    def forbidden_super_user_role_update_response(self, user):
        """Method that returns unauthorized super user role update response"""
        return {
            "Message": user + " role can not be updated"}, 403
