from flask import session

tags = (session['tags'])['tags']
keys = []
values = []

for each in tags:
    key= [k for (k,v) in each.items()]
    keys.append(key)
    value= [v for (k,v) in each.items()]
    values.append(value)

tags = {}

for k,v in zip(keys,values):
    tags[k[0]]=v[0]

URL_API= 'https://growmer.com/api/beta/'

login = {
    "USERNAME_INPUT": (tags['USERNAME_INPUT'])['tag'], #css yes
    "PASSWORD_INPUT": (tags['PASSWORD_INPUT'])['tag'], #css yes
    "LOGIN_BUTTON": (tags['LOGIN_BUTTON'])['tag'], #xpath yes
    "NOT_NOW": (tags['NOT_NOW'])['tag'], #xpath yes
    "CHANGE_ACCOUNT": (tags['CHANGE_ACCOUNT'])['tag'], #xpath yes
    "USERNAME": (tags['USERNAME'])['tag'], #css
}

get_unfollowers ={
    "FOLLOWING_BUTTON": (tags['FOLLOWING_BUTTON'])['tag'], #xpath yes
    "N_FOLLOWING": (tags['N_FOLLOWING'])['tag'], #xpath yes
    "FOLLOWERS_BUTTON": (tags['FOLLOWERS_BUTTON'])['tag'], #xpath yes
    "N_FOLLOWERS": (tags['N_FOLLOWERS'])['tag'] #xpath yes
} 

get_names ={
    "SCROLL_BOX": (tags['SCROLL_BOX'])['tag'], #css yes
    "CLOSE_BUTTON": (tags['CLOSE_BUTTON'])['tag'], #css yes
}

unfollow_with_username = {
    "FOLLOW_BUTTON" : (tags['FOLLOW_BUTTON'])['tag'], #xpath yes
    "UNFOLLOW_BUTTON" : (tags['UNFOLLOW_BUTTON'])['tag'], #xpath yes
    "CONFIRMBUTTON" : (tags['CONFIRMBUTTON'])['tag'] #xpath yes
}

public_account ={
    "PUBLIC_ACCOUNT": (tags['PUBLIC_ACCOUNT'])['tag'] #css yes
}

input_search ={
    "HASHTAG_INPUT": (tags['HASHTAG_INPUT'])['tag'], #css
    "HASHTAG_INPUT_B": (tags['HASHTAG_INPUT_B'])['tag'] #css yes
}


follow_strategy ={
    "POST_TO_SCRAPE": (tags['POST_TO_SCRAPE'])['tag'],#css yes
    "LIKE_LIST": (tags['LIKE_LIST'])['tag'], #css yes
    "PROFILE_LIST": (tags['PROFILE_LIST'])['tag'], #css yes
    "N_POST": (tags['N_POST'])['tag'], #xpath yes
    "N_FOLLOWING": (tags['N_FOLLOWING'])['tag'], #xpath yes
    "N_FOLLOWERS": (tags['N_FOLLOWERS'])['tag'], #xpath yes
    "FOLLOW_BUTTON": (tags['FOLLOW_BUTTON'])['tag'], #xpath yes  
    "CLOSE_BUTTON": (tags['CLOSE_BUTTON'])['tag'], #css yes
    "HOME_IG": (tags['HOME_IG'])['tag'] #css yes
}

get_info_profile ={
    "N_POST": (tags['N_POST'])['tag'], #xpath yes
    "N_FOLLOWERS": (tags['N_FOLLOWERS'])['tag'], #xpath yes
    "N_FOLLOWING": (tags['N_FOLLOWING'])['tag'], #xpath yes
    "POST_TO_SCRAPE": (tags['POST_TO_SCRAPE'])['tag'], #css yes
    "TIME_FROM_PUBLISH": (tags['TIME_FROM_PUBLISH'])['tag'], #css yes
    "LIKES": (tags['LIKES'])['tag'], #xpath yes
    "MORE_COMMENTS": (tags['MORE_COMMENTS'])['tag'], #css yes
    "UL_COMMENT": (tags['UL_COMMENT'])['tag'], #css yes
    "NEXT_POST_USER": (tags['NEXT_POST_USER'])['tag'], #xpath yes
    
}

get_followers = {
    'N_FOLLOWERS': (tags['N_FOLLOWERS'])['tag'], #xpath yes
    'FOLLOWERS_BUTTON': (tags['FOLLOWERS_BUTTON'])['tag'], #xpath yes
}

change_account ={
    'IMG_DROP': (tags['IMG_DROP'])['tag'], #css yes
    'EXIT': (tags['EXIT'])['tag'], #xpath yes
    'LOGOUT': (tags['LOGOUT'])['tag']#xpath yes
}
