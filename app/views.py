from flask import redirect, Blueprint

root_blueprint = Blueprint('root', __name__)

@root_blueprint.route('/')
def index():
    return redirect('https://adcstoremanagerapiv2.docs.apiary.io')