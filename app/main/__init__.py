from flask import Blueprint

main = Blueprint('main', __name__)

from .views import login,login_ig, not_follow_back, seguir, seguir_advanced, unfollow, unfollow_list
