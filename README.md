# Project report - YAAS 2019

Author: Otto Lindfors 37944
## Implemented requirements and passed tests

### Very important information
I have configured the app so that it by default will ask for confirmation when creating an auction. But this
makes almost all the tests fail. Therefore I have made it easy for you to turn off the confirmation. When 
turned off all tests listed below will pass.  
  
**To turn of the create-auction-confirmation** navigate the project files to:  
`auction.views.CreateAuction.post()` on `row 83` and set `ask_for_confirmation = True`.

### List of implemented requirements and passed tests
* UC1
  * Full functionality and all requirements implemented.
  * All tests are passed
  * See conflicts in requirements below.
  * 1 p.
* UC2
  * Full functionality and all requirements implemented.
  * All tests are passed
  * 1 p.
* UC3
  * Full functionality and all requirements implemented.
  * All tests are passed
  * See conflicts between test and requirement below.
  * 3 p.
* UC4
  * Full functionality and all requirements implemented.
  * All tests are passed  
  * 1 p.
* UC5
  * Full functionality and all requirements implemented.
  * All tests are passed 
  * 1 p. 
* UC6
  * Full functionality and all requirements implemented.
  * All tests are passed
  * See conflicts with requirements below.
  * 3 p.  
* UC7 
  * Full functionality and all requirements implemented.
  * All tests are passed
  * 1 p.
* UC9
  * Full functionality and all requirements implemented.
  * Test do not pass. See conflicts with requirements below.
  * 2 p.
* REQ 9.3
  * Full functionality and all requirements implemented.
  * No test provided
  * 1 p.
* UC10
  * Full functionality and all requirements implemented.
  * See conflicts between test and requirement below.
  * 2 p.
* WS1
  * Full functionality and all requirements implemented.
  * All tests are passed
  * 2 p.
* WS2
  * See conflicts between test and requirement below.

  
## Conflicts in requirements and tests
* UC1
  * (Not really an issue)
  * Constraint:  
  ​We assume that administrator accounts are created using the Django admin interface. For this, you must 
  enable the Django admin interface in your project.
  * Conflict:  
  One cannot access the admin interface without first creating a superuser. Therefore a superuser needs 
  to be created using manage.py.
  * Solution:  
  Create admin (superuser) using Django’s command-line utility for admin tasks (manage.py and django-admin).

* REQ3.3, REQ3.3.1, REQ3.3.2
  * ​Requirement:  
  The user must be asked for a confirmation before creating a new auction.
  * Conflict:  
  The testTDD only works without the confirmation. Therefore the confirmation can be disabled.
  * Solution:  
  To enable/disable confirmation toggle the variable in auction > views > CreateAuction > post() > ask_for_confirmation = True/False

* UC6 & UC10
  * Requirement:  
  The application must show the most recent description of the auction before accepting bids from the user.
  An error message "there is a newer version of the auction" should not be shown to the user.
  * Conflict:  
  This would only work if the user is bidding via the browser. The user would have to GET the auction before
  POSTing because otherwise one cannot know what version/revision of the auction the user is viewing, so to speak. If the user directly
  POST a bid on a auction the generic error message "there is a newer version of the auction" should not be shown as the
  bid might simply be too low and therefore the error message is misleading!
  * Implementation and workaroud (hope it makes sense. You will get it when you use the app):  
    * The application is now implemented so that when a user GET the bidding page
    the auction version number is stored to the users session (on the server). When the user POST 
    a bid the version number is compared to the auctions current version number before the 
    bid is accepted.  
    * There is potential for issues with this solution and therefore when I create a web page 
    that will be in actual use this solution is not one I would use.  
    * The potential issue is the following. Imagine a user GET the bidding page. The version 
    number of the viewed auction is stored on the server. The user leaves the page without 
    POSTing a bid. Later the same user places a bid via a POST request (without 
    first GETing the page, e.g. if the user has viewed another bid in a new tab in between). Well, now the server will not accept the bid since the version number
    associated with the user is old.
    * WORKAROUND:  
    The issue is partially worked around in the following way. As a user POST a bid the
    version number will be checked. The function that get the version number from the user
    session will clean up the session data so that it removes the stored version number after
    it has retrieved it. This way if the POST is rejected due to the old version number the
    user just need to try again (POST again) as the old version number got cleaned out 
    from the session when it was compared after the first POST request. For the user in the 
    browser this means pressing the 'bid' button again.  
    This is of course a very ugly solution, but then again, this website is not intended to
    be used in production.
    
* UC9
  * Requirement:  
  Status code `200` after successful change of language
  * Conflict:  
  I have a link (url) the user clicks to change the language. In the method that changes the language I use 
  `return redirect(request.META['HTTP_REFERER'])` to reload the previous page (from where the user clicked the link)
  so that the changes take effect. This will give status code `302` and then `200`. The full functionality is 
  still implemented.  
  An alternative solution would have been to reload the page using javascript but that is not in the scope of this 
  course.

* WS2
  * Requirent:
    * The error messages should be:    
      1. “Cannot bid on own auction”  
      2. “Can only bid on active auction”
      3. “New bid must be greater than the current bid at least 0.01”
  * Conflict:
    * The error messages are:
      1. “You cannot bid on own auction”  
      2. “You can only bid on active auction”
      3. “New bid must be greater than the current bid for at least 0.01”
  * Solution:  
    * This is not an issue.
    * Since it is the same method that do the actual posting for the API as for the non-API 
    the error messages are the same. Therefore the error messages do not match the requirements 
    exactly.

## Brower used for testing
* Firefox 70.0 on macOS Catalina 10.15 and Ubuntu 18.04 LTS

## List of installed Python packages
Django==2.2.5  
djangorestframework==3.10.3  
freezegun==0.3.12  
requests==2.22.0  

## Other packages
gettext==0.20.1


# Instructions for gettext on macOS

All the commands in these instructions are meant to be run in a terminal. 
These instructions where made on macOS Catalina using zsh but they should work in bash as well and probably 
also in some other shells.

## Install Homebrew
Using Homebrew is by far the easiest way to cleanly install and cleanly uninstall gettext. Using Homebrew won't 
mess up or even touch macOS's default gettext packages as it installs everyting in an isolated folder.

Follow the instructions on https://brew.sh/  
```/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"```

If you like to opt-out from Homebrew's analytics use  
```brew analytics off```

## Install gettext
Install gettext with homebrew  
```brew install gettext```

After the installation Homebrew will give the following notice
>gettext is keg-only, which means it was not symlinked into /usr/local,
>because macOS provides the BSD gettext library & some software gets confused if both are in the library path.

In order to use gettext one needs to add that path variable that Homebrew is talking about. I will add it to my 
virtual environment so that it will be available from within my virtual environment.  

Add the following lines to `.virtualenvs/postactivate`  
```
# This is for gettext to work (installed with Homebrew)
export TEMP_PATH=$PATH
export PATH=$PATH:/usr/local/Cellar/gettext/0.20.1/bin
```

Add the following lines to `.virtualenvs/postdeactivate`  
```
# This is for gettext to work (installed with Homebrew)
export PATH=$TEMP_PATH
unset TEMP_PATH
```
 
## Compile languages (use gettext)
PyCharm will not (for some reason) find gettext when you run `makemessages -l sv` from the `manage.py` task. Therefore 
you need to run the `manage.py` task yourself from within your virtualenvironment.  

Do the following. (I assume you have virtualenv and virtualenvwrapper installed, although virtualenvwrapper is not 
necessary it is a nice set of shorthand commands.)

Activate your virtual environment:  
```
otto@dyn-vpn-218-048 ~ %
workon yaas-project-2019-ottolindfors
```

`manage.py` is located in the root of your project, so navigate there. For me it is `cd PycharmProjects/yaas-project-2019-ottolindfors/`:  
```
(yaas-project-2019-ottolindfors) otto@dyn-vpn-218-048 ~ % cd PycharmProjects/yaas-project-2019-ottolindfors/
```  

You can double check that you are in the correct folder by listing the content of the folder with `ls`. 
My project folder contains:  
```
(yaas-project-2019-ottolindfors) otto@dyn-vpn-218-048 yaas-project-2019-ottolindfors % ls
README.md		backlog			requirements.txt
README_original.md	db.sqlite3		templates
__pycache__		locale			user
auction			manage.py		yaas
```

Now you can create the translations with `python manage.py makemessages -l sv`:
```
(yaas-project-2019-ottolindfors) otto@dyn-vpn-218-048 yaas-project-2019-ottolindfors % python manage.py makemessages -l sv  
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
processing locale sv
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
Warning: Failed to set locale category LC_NUMERIC to en_FI.
Warning: Failed to set locale category LC_TIME to en_FI.
Warning: Failed to set locale category LC_COLLATE to en_FI.
Warning: Failed to set locale category LC_MONETARY to en_FI.
Warning: Failed to set locale category LC_MESSAGES to en_FI.
```

And compile the translated messages with `python manage.py compilemessages`: 

```
(yaas-project-2019-ottolindfors) otto@dyn-vpn-218-019 yaas-project-2019-ottolindfors % python manage.py compilemessages
processing file django.po in /Users/otto/PycharmProjects/yaas-project-2019-ottolindfors/locale/sv/LC_MESSAGES
```
