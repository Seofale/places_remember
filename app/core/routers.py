from flask import Blueprint, render_template, url_for, redirect, flash, request, Response
from flask_login import login_user, logout_user, current_user, login_required

from app.core.oauth import OAuth2SignIn
from app.core.models import db, User, Place
from app.core.config import APIKEY_YANDEX

bp = Blueprint('home', __name__, url_prefix='')


@bp.route('/')
def index():
    if current_user.is_authenticated:
        places = Place.query.filter_by(user=current_user).order_by(Place.added_at.desc()).all()
        return render_template('index.html', places=places)
    return render_template('index.html')


@bp.route('/add-place')
@login_required
def show_add_place_form():
    return render_template('add_place_form.html', apikey=APIKEY_YANDEX)


@bp.route('/save-place', methods=['POST'])
@login_required
def save_place():
    place_data = request.get_json()
    if place_data.get('address') and place_data.get('title') and place_data.get('comment'):
        place = Place(
            address=place_data.get('address'),
            title=place_data.get('title'),
            comment=place_data.get('comment')
        )
        place.user = current_user
        db.session.add(place)
        db.session.commit()
        return Response(status=201)

    return Response(status=400)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.index'))


@bp.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))

    oauth = OAuth2SignIn.get_provider_class_instance(provider)

    return oauth.authorize()


@bp.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('home.index'))

    oauth = OAuth2SignIn.get_provider_class_instance(provider)
    social_id, fullname, photo = oauth.callback()
    if social_id is None:
        flash('При авторизации произошла ошибка')
        return redirect(url_for('home.index'))

    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, fullname=fullname, photo=photo)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)

    return redirect(url_for('home.index'))
