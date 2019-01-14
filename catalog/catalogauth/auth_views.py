from catalog.catalogapi.models import db, User, OAuth
from catalog.catalogauth import bp
from flask import flash, url_for, redirect
from flask_login import login_required, login_user, logout_user
from catalog import google_bp
from flask_dance.consumer import oauth_authorized
from sqlalchemy.orm.exc import NoResultFound


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have logged out")
    return redirect(url_for('catalogapp.index'))


@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google API.", category="error")
        return False
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        msg = "Failed to fetch user info from Google API."
        flash(msg, category="error")
        return False
    google_info = resp.json()
    google_user_id = str(google_info["id"])
    google_user_email = google_info["email"]
    google_user_picture = google_info["picture"]

    # Find this Oauth token in the DB, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name,
        provider_user_id=google_user_id,
    )
    try:
        oauth = query.one()
    except NoResultFound:
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            token=token,
        )
    if oauth.user:
        login_user(oauth.user)
        flash("Successfully signed in with Google API.")
    else:
        user = User(
            username=google_user_email,
            email=google_user_email,
            picture=google_user_picture,
            role='User',

        )
        # Associate the new local user account with the OAuth token
        oauth.user = user
        # Save and commit our database models
        db.session.add_all([user, oauth])
        db.session.commit()
        # Log in the new or existing local user account
        login_user(user)
        flash("Succesfully signed in with Google API.")
    # Disable Flask-Dance's default behavior for saving the OAuth token
    return False
