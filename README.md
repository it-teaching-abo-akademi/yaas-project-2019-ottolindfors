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
* UC10
  * Full functionality and all requirements implemented.
  * See conflicts between test and requirement below.
## Conflicts between requirements and tests
* REQ3.3, REQ3.3.1, REQ3.3.2
  * ​Requirement: The user must be asked for a confirmation before creating a new auction.
  * Conflict: The testTDD only works without the confirmation. Therefore the confirmation is disabled.
  To enable confirmation toggle the variable auction > views > CreateAuction > post() > ask_for_confirmation = True

* UC10
  * Requirement: The application must show the most recent description of the auction before accepting bids from the user.
  An error message "there is a newer version of the auction" should not be shown to the user.
  * Conflict: This would only work if the user is bidding via the browser. The user would have to GET the auction before
  POSTing because otherwise one cannot know what version/revision of the auction the user is viewing. If the user directly
  POST a bid on a auction the generic error message "there is a newer version of the auction" should not be shown as the
  bid might simply be too low and therefore the error message is misleading!

## Brower used for testing
* Firefox 69.0.2 on macOS and Ubuntu 18.04 LTS

## List of Python packages
* See requirements.txt