import secrets, os
from PIL import Image
from Site.models import User
from flask import redirect, url_for, flash, current_app
from flask_mail import Message
from Site import mail

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_fn)
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def send_reset_email(user:User):
    try:
        token = user.get_reset_token()
        msg = Message('Password reset', recipients=[user.email])

        msg.body = f''' to reset you'r password visit the following link:
{url_for('users.reset_password', token=token, _external=True)}
    
If you did not make this request then simply ignore this email
    '''
        mail.send(msg)
    except Exception as e:
        flash(f"Error sending email: {str(e)}", 'danger')
        return redirect(url_for('users.login'))