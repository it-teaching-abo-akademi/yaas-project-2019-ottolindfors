# Project report - YAAS 2019

Author: Otto Lindfors 37944
## Implemented requirements
## Passed tests
* UC1
  * Full functionality and all requirements implemented.
  * All tests are passed  
* UC2
  * Full functionality and all requirements implemented.
  * All tests are passed  
* UC3
  * Full functionality and all requirements implemented.
  * All tests are passed
  * See conflicts between test and requirement below.  
* UC4
  * Full functionality and all requirements implemented.
  * All tests are passed  
* UC5
  * Full functionality and all requirements implemented.
  * All tests are passed  
* UC6
  * Full functionality and all requirements implemented.
  * All tests are passed
  * See conflicts with requirements below.  
* UC10
  * Full functionality and all requirements implemented.
  * See conflicts between test and requirement below.  
  
## Conflicts between requirements and tests
* REQ3.3, REQ3.3.1, REQ3.3.2
  * ​Requirement:  
  The user must be asked for a confirmation before creating a new auction.
  * Conflict:  
  The testTDD only works without the confirmation. Therefore the confirmation is disabled.
  To enable confirmation toggle the variable auction > views > CreateAuction > post() > ask_for_confirmation = True

* UC6 & UC10
  * Requirement:  
  The application must show the most recent description of the auction before accepting bids from the user.
  An error message "there is a newer version of the auction" should not be shown to the user.
  * Conflict:  
  This would only work if the user is bidding via the browser. The user would have to GET the auction before
  POSTing because otherwise one cannot know what version/revision of the auction the user is viewing. If the user directly
  POST a bid on a auction the generic error message "there is a newer version of the auction" should not be shown as the
  bid might simply be too low and therefore the error message is misleading!
  * Implementation and workaroud:  
    * The application is now implemented so that when a user GET the bidding page
    the auction version number is stored to the users session (on the server). When the user POST 
    a bid the version number is compared to the auctions current version number before the 
    bid is accepted.  
    * There is potential for issues with this solution and therefore when I create a web page 
    that will be in actual use this solution is not one I would use.  
    * The potential issue is the following. Imagine a user GET the bidding page. The version 
    number of the viewed auction is stored on the server. The user leaves the page without 
    POSTing a bid. Later the same user places a bid manually via a POST request (without 
    first GETing the page). Well, now the server will not accept the bid since the version number
    associated with the user is old.
    * WORKAROUND:  
    The issue is partially worked around in the following way. As a user POST a bid the
    version number will be checked. The function that get the version number from the user
    session will clean up the session data so that it removes the stored version number after
    it has gotten it. This way if the POST is rejected due to the old version number the
    user just need to try again (POST again) as the old version number got cleaned out 
    from the session when it was compared after the first POST request. For the user in the 
    browser this means pressing the 'bid' button again.  
    This is of course a very ugly solution, but then again this website is not intended to
    be used in production.
  

## Brower used for testing
* Firefox 70.0 on macOS Catalina and Ubuntu 18.04 LTS

## List of Python packages
* See requirements.txt