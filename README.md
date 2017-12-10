# VersionTracker

VersionTracker is a webapp where you can search softwares and know whether the version you are using is outdated or not. The 
app will list the various versions of the software that has been released and the number of versions which has been relaased
after the version you are using. The app also suggests you alternative softwares which you may consider using.

## Stack used
- Flask : Webframework in Python
- Postgres : Database
- BeautifulSoup : Webscraping
- Jinja : Templating language
- flask-admin : For craeting admin
- flask-login : For creating auth system
- SQLAlchemy : ORM
- MaterialiseCSS : For UI
- gunicorn : Web Server
- Heroku : Deployment

## REST API
VersionTracker provides a RESTful service. The following endpoint is provided -
**METHOD : GET**
https://version-tracker.herokuapp.com/version_track/api?name=[software_name]&version=[software_version]
For example: 
https://version-tracker.herokuapp.com/version_track/api?name=firefox&version=55

**Output**
```
{
  "initial_release": "Released: 03 May 2013 (4 years 7 months ago)\r\n", 
  "latest_version": "Skype 7.40.0.103", 
  "name": "skype", 
  "number_of_versions": 78, 
  "similar_softwares": [
    "skype for business", 
    "discord", 
    "facetime", 
    "hangouts", 
    "viber", 
    "zoom", 
    "whatsapp", 
    "google voice", 
    "webex", 
    "slack"
  ], 
  "software_found": "FOUND", 
  "version_found": "NOT_FOUND", 
  "versions": [
    "Skype 7.40.0.103", 
    "Skype 7.39.0.102", 
    "Skype 7.38.0.101", 
    "Skype 7.37.0.103", 
    "Skype 7.36.0.101", 
    "Skype 7.35.0.103", 
    "Skype 7.35.0.102", 
    "Skype 7.35.0.101", 
    "Skype 7.34.0.103", 
    "Skype 7.34.0.102", 
    "Skype 7.34.0.102", 
    "Skype 7.33.0.105", 
    "Skype 7.32.0.104", 
    "Skype 7.32.0.103", 
    "Skype 7.30.80.105", 
    "Skype 7.30.85.103", 
    "Skype 7.29.0.102", 
    "Skype 7.28.0.101", 
    "Skype 7.27.0.101", 
    "Skype 7.26.0.101", 
    "Skype 7.25.0.106", 
    "Skype 7.25.0.106", 
    "Skype 7.25.0.103", 
    "Skype 7.24.0.104", 
    "Skype 7.23.0.105", 
    "Skype 7.23.0.104", 
    "Skype 7.22.0.109", 
    "Skype 7.22.0.108", 
    "Skype 7.22.0.107", 
    "Skype 7.22.0.104", 
    "Skype 7.21.0.100", 
    "Skype 7.18.0.112", 
    "Skype 7.18.0.112", 
    "Skype 7.18.0.111", 
    "Skype 7.18.0.109", 
    "Skype 7.18.0.103", 
    "Skype 7.17.0.106", 
    "Skype 7.17.0.105", 
    "Skype 7.17.0.104", 
    "Skype 7.16.0.102", 
    "Skype 7.16.0.101", 
    "Skype 7.15.0.103", 
    "Skype 7.15.0.102", 
    "Skype 7.15.0.102", 
    "Skype 7.14.0.105", 
    "Skype 7.14.0.104", 
    "Skype 7.13.0.101", 
    "Skype 7.12.0.101", 
    "Skype 7.11.0.102", 
    "Skype 7.10.0.101", 
    "Skype 7.9.0.103", 
    "Skype 7.8.0.102", 
    "Skype 7.7.0.103", 
    "Skype 7.7.0.102", 
    "Skype 7.7.0.102", 
    "Skype 7.6.0.105", 
    "Skype 7.6.0.103", 
    "Skype 7.5.0.102", 
    "Skype 7.5.0.101", 
    "Skype 7.4.0.102", 
    "Skype 7.3.0.101", 
    "Skype 7.2.0.103", 
    "Skype 7.1.0.105", 
    "Skype 7.0.0.102", 
    "Skype 7.0.0.100", 
    "Skype 7.0.0.100", 
    "Skype 6.22.64.107", 
    "Skype 6.22.64.106", 
    "Skype 6.22.81.105", 
    "Skype 6.22.81.104", 
    "Skype 6.21.0.104", 
    "Skype 6.20.0.104", 
    "Skype 6.18.0.106", 
    "Skype 6.18.0.105", 
    "Skype 6.16.0.105", 
    "Skype 6.14.0.104", 
    "Skype 6.14.0.104", 
    "Skype 6.5.0.107 Beta"
  ]
}
```
## How to use the Web app
<table>
<tr>
<td><img src="screenshots/vt_main.png"><br/>Store listing page</td>
</tr>
<tr>
<td><img src="screenshots/vt_result.png"><br/>App information</td>
</tr>
</table>

Enter the name of your software and version in the respective fields and press search. Wait for some time as it may take a while to generate your result. Once the result is generated, it will be displayed on screen. You will be informed whether version is obsolete or not. How many new versions have been released. What was the initial release date of the software.
What is the latest version available.
You can also view all the versions of the software relased by pressing on View all releases.
<table>
<tr>
<td><img src="screenshots/vt_versions.png"><br/>Store listing page</td>
</tr>
</table>




