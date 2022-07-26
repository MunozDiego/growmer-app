from app import db
from datetime import datetime

class FollowsData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ig_username = db.Column(db.String(255), unique = True,  nullable = False)
    campaing = db.Column(db.Integer, db.ForeignKey('bot_campaing.id'))

class BotCampaing(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    str_date = db.Column(db.String())
    n_follows = db.Column(db.Integer)
    follows_back = db.Column(db.Integer)
    update_date = db.Column(db.DateTime())
    duration = db.Column(db.Integer)
    users_following =  db.relationship('FollowsData', backref='follows_data', lazy='dynamic')
    status = db.Column(db.String)
    auto_unfollow = db.Column(db.Integer, default=0)
    unfollow = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user_personal_data.id'))

class UserPersonalData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    ig_username = db.Column(db.String(255), unique = True,  nullable = False)
    data =  db.relationship('AccountsData', backref='account_data', lazy='dynamic')
    campaings =  db.relationship('BotCampaing', backref='campaing_data', lazy='dynamic')

    def __repr__(self):
        return '<%r>' % self.ig_username

class AccountsData(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    str_date = db.Column(db.String())
    account = db.Column(db.Integer, db.ForeignKey('user_personal_data.id'))
    followers = db.Column(db.Integer)
    following = db.Column(db.Integer)
    posts = db.Column(db.Integer)
    likes_prom = db.Column(db.Integer)
    comment_prom = db.Column(db.Integer)
    Plumer_rate = db.Column(db.Float)

    def to_dict(self):
        return dict(id=self.id,
                    created_at=self.date.strftime('%d %B'),
                    followers = self.followers,
                    following = self.following,
                    posts = self.posts,
                    likes_prom = self.likes_prom,
                    comment_prom = self.comment_prom,
                    plumer_rate = self.Plumer_rate)

    def __repr__(self):
        return '<Get at %r>' % self.date
