# Growmer App

## Instagram automation tool based on Flask and Selenium

This project was made with Flask, and the goal is to build a desktop app with the Chromium Embedded Framework browser, which is a minimalist version of Chromium. In order to build a desktop app with Python and web technologies flexibilities, we must to implement something similar to Jupyter Notebooks, but instead of use Chrome, We will open the Flask server in CEF browser from Python. then we make a .exe file with something like pyinstaller.

I use the following command to make the .exe

### `pyinstaller --noconsole --noupx -F -i "logo_fav.ico" --add-data "app/templates;app/templates" --add-data "app/static;app/static" --add-data "ChromeDriver;ChromeDriver" --add-data "cefsimple;cefsimple" -n Growmer run.py`

To make it work, we need to add a build of CEF in the root directory of the app, since this app is a Instagram bot build upon Selenium, we also need to add the driver. The folder structure must look like the below.

├───app
│   ├───main
│   │   └───views
│   │  
│   ├───static
│   │   ├───css
│   │   ├───img
│   │   ├───js
│   │   └───vendor     
│   │       
│   └───templates
│   
├───cefsimple   
│       
└───ChromeDriver
    
The App had a login form wich authenticates the user with http basic auth in the Growmer API, then retrieve the selectors and xpath to interact with the elements in The Instagram DOM through Selenium. 

NOTE: The Growmer web is Currently unavailable, may be I make it work with serverless API running upon lambda function, dynamoDb and AWS Cognito.



