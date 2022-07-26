import os
import sys
import subprocess
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import config

db = SQLAlchemy()

def create_app(config_name):

    app = Flask(__name__)

    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    db.init_app(app)

    def resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
            return os.path.join(base_path, relative_path)
        except Exception:
            return relative_path
    
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.common.exceptions import WebDriverException


    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:5351")
    try:
        browser = webdriver.Chrome(resource_path('ChromeDriver/89/chromedriver.exe'),options=chrome_options)
    except WebDriverException:
        try:
            browser = webdriver.Chrome(resource_path('ChromeDriver/88/chromedriver.exe'),options=chrome_options)
        except WebDriverException:
            browser = webdriver.Chrome(resource_path('ChromeDriver/90/chromedriver.exe'),options=chrome_options)
    app.browser = browser

    from app.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')
    
    path = resource_path(relative_path='cefsimple/Debug/cefsimple.exe')
    app.cef_process = subprocess.Popen([f'{path}', '--url=localhost:7481/login'], 
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        stdin=subprocess.PIPE,
                        universal_newlines=True)

    return app