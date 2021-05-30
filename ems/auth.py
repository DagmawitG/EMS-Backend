from flask import Blueprint, request, jsonify, abort
from functools import wraps
from ems import db
from flask_login import login_user, current_user, logout_user
from ems.models import *

bp = Blueprint('auth', __name__)