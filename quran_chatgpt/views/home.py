from flask import Blueprint

home = Blueprint(
    'home',
    __name__
)

@home.route('/', methods=['GET', 'POST'])
def home_route():
    return 'OK', 200
