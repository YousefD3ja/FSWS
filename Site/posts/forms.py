from flask_wtf import FlaskForm, Form
from wtforms import StringField, SubmitField, TextAreaField, FieldList, FormField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    picture0 = FileField("", validators=[FileAllowed(['png', 'jpg'])])
    picture1 = FileField("", validators=[FileAllowed(['png', 'jpg'])])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField("CreatePost")
