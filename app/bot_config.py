

login = {
    "USERNAME_INPUT": "input[name='username']", #css
    "PASSWORD_INPUT": "input[name='password']", #css
    "LOGIN_BUTTON": "//button[@type='submit']", #xpath
    "NOT_NOW": "//button[contains(text(), 'Ahora no')]", #xpath
    "CHANGE_ACCOUNT": "//button[contains(text(), 'Cambiar de cuenta')]", #xpath
    "USERNAME": "a[class='gmFkV']", #css
}


get_unfollowers ={
    "FOLLOWING_BUTTON": "//a[contains(@href,'/following')]", #xpath
    "N_FOLLOWING": '//section/ul/li[3]/a/span', #xpath
    "FOLLOWERS_BUTTON": "//a[contains(@href,'/followers')]", #xpath
    "N_FOLLOWERS": '//section/ul/li[2]/a/span' #xpath
} 

get_names ={
    "SCROLL_BOX": "div[class='isgrP']", #css
    "CLOSE_BUTTON": "svg[aria-label='Cerrar']", #css
}

unfollow_with_username = {
    "FOLLOW_BUTTON" : "//button[text() = 'Seguir']", #xpath
    "UNFOLLOW_BUTTON" : "span[aria-label='Siguiendo']", #css
    "CONFIRMBUTTON" : "//button[text() = 'Dejar de seguir']" #xpath
}

public_account ={
    "PUBLIC_ACCOUNT": "//h2[text()='Esta cuenta es privada']" #css
}

input_search ={
    "HASHTAG_INPUT": "input[placeholder='Buscar']", #css
    "HASHTAG_INPUT_B": "input[placeholder='Busca']" #css

}


follow_strategy ={
    "POST_TO_SCRAPE": "div[class='v1Nh3 kIKUG  _bz0w']",#css
    "LIKE_LIST": "//a[text() = ' Me gusta']", #xpath
    "PROFILE_LIST": "div[class='_7UhW9   xLCgt      MMzan  KV-D4          uL8Hv         ']", #css
    "N_POST": "//header/section/ul/li/span/span", #xpath
    "N_FOLLOWERS": '//section/ul/li[2]/a/span', #xpath       NO
    "N_FOLLOWING": '//section/ul/li[3]/a/span', #xpath       NO
    "FOLLOW_BUTTON": '//button[text() = "Seguir"]', #xpath      NO 
    "CLOSE_BUTTON": 'svg[aria-label="Cerrar"]', #css    NO
    "HOME_IG": "div[class='oJZym']" #css
}

get_info_profile ={
    "N_POST": '//header/section/ul/li/span/span', #xpath     NO
    "N_FOLLOWERS": '//section/ul/li[2]/a/span', #xpath    NO
    "N_FOLLOWING": '//section/ul/li[3]/a/span', #xpath    NO
    "POST_TO_SCRAPE": 'div[class="v1Nh3 kIKUG  _bz0w"]', #css    NO
    "TIME_FROM_PUBLISH": 'time', #css
    "LIKES": '//button/span', #xpath
    "MORE_COMMENTS": "span[aria-label = 'Load more comments']", #css
    "UL_COMMENT": "ul[class = 'Mr508']", #css
    "NEXT_POST_USER": "//a[text() = 'Siguiente']", #xpath
    
}

get_followers = {
    'N_FOLLOWERS': '//section/ul/li[2]/a/span', #xpath      NO
    'FOLLOWERS_BUTTON': "//a[contains(@href,'/followers')]", #xpath      NO
}

change_account ={
    'IMG_DROP':"nav[class='NXc7H jLuN9  '] img[data-testid='user-avatar']", #css
    'EXIT': "//div[text()='Salir']",
    'LOGOUT': "//div[text()='Cerrar sesión']"
}