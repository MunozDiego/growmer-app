from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, BooleanField, IntegerField,TextAreaField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, NumberRange
from wtforms import ValidationError

class UserLogin(FlaskForm):
    username = StringField('user mail', validators=[DataRequired(),Regexp(r'^[\w.@+-]+$'), Length(1, 64)])
    email = StringField('Email', validators=[DataRequired(),Regexp(r'^[\w.@_-]+$'), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
    
class UserLoginIg(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Ingresar')
    

class UserFollow(FlaskForm):
    seed = StringField('Hashtag', validators=[DataRequired()])
    n_follows = IntegerField('Numero de usuarios a seguir', validators=[DataRequired(),NumberRange(min=1, max=200, message='No puedes sobrepasar el límite de 200 usuarios al día.')])
    submit = SubmitField('Iniciar')

class UserFollowAdvanced(FlaskForm):
    seed = StringField('Hashtag', validators=[DataRequired()])
    n_follows = IntegerField('Numero de usuarios a seguir', validators=[DataRequired(),NumberRange(min=1, max=200, message='No puedes sobrepasar el límite de 200 usuarios al día.')])
    n_min_followers = IntegerField('n° minimo de seguidores', default = 30,validators=[NumberRange(min=0, max=9999, message='Este campo debe estar entre 0 y 9999')])
    n_max_followers = IntegerField('n° maximo de seguidores', default = 1500,validators=[NumberRange(min=0, max=9999, message='Este campo debe estar entre 0 y 9999')])
    post_min_requirement = IntegerField('n° minimo de post', default = 3)
    delta_down = StringField('Porcentage de seguidores respecto a seguidos', default = '60%')
    delta_up = IntegerField('maximo numero de seguidores por sobre el n° de seguidos', default = 800, validators=[NumberRange(min=0, max=9999, message='Este campo debe estar entre 0 y 9999')])
    n_max_following = IntegerField('numero maximo de seguidos', default = 2000,validators=[NumberRange(min=0, max=9999, message='Este campo debe estar entre 0 y 9999')])
    time_lag_up = IntegerField('Limite superior de rango de espera entre seguidos', default = 60)
    time_lag_down = IntegerField('Limite inferior de rango de espera entre seguidos', default = 20)
    submit = SubmitField('Iniciar')

class UserUnfollowAuto(FlaskForm):
    date = SelectField('Fecha', choices=[],coerce=int)
    unfollow_all = BooleanField('Dejar de seguir a todos los que seguiste en el dia seleccionado',default="checked")
    submit = SubmitField('Iniciar')

class UserUnfollowListText(FlaskForm):
    user_list = TextAreaField('Lista de usuarios', validators=[DataRequired()])
    submit = SubmitField('Iniciar')

class UploadForm(FlaskForm):
    list_file        = FileField('List File', validators=[FileRequired(), FileAllowed(['csv', 'json'], 'csv or json format only!')])


class NotFollowBack(FlaskForm):
    submit = SubmitField('Obtener')
