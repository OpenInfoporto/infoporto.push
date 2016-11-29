# ============================================================================
# DEXTERITY ROBOT TESTS
# ============================================================================
#
# Run this robot test stand-alone:
#
#  $ bin/test -s infoporto.push -t test_device.robot --all
#
# Run this robot test with robot server (which is faster):
#
# 1) Start robot server:
#
# $ bin/robot-server --reload-path src infoporto.push.testing.INFOPORTO_PUSH_ACCEPTANCE_TESTING
#
# 2) Run robot tests:
#
# $ bin/robot src/plonetraining/testing/tests/robot/test_device.robot
#
# See the http://docs.plone.org for further details (search for robot
# framework).
#
# ============================================================================

*** Settings *****************************************************************

Resource  plone/app/robotframework/selenium.robot
Resource  plone/app/robotframework/keywords.robot

Library  Remote  ${PLONE_URL}/RobotRemote

Test Setup  Open test browser
Test Teardown  Close all browsers


*** Test Cases ***************************************************************

Scenario: As a site administrator I can add a Device
  Given a logged-in site administrator
    and an add device form
   When I type 'My Device' into the title field
    and I submit the form
   Then a device with the title 'My Device' has been created

Scenario: As a site administrator I can view a Device
  Given a logged-in site administrator
    and a device 'My Device'
   When I go to the device view
   Then I can see the device title 'My Device'


*** Keywords *****************************************************************

# --- Given ------------------------------------------------------------------

a logged-in site administrator
  Enable autologin as  Site Administrator

an add device form
  Go To  ${PLONE_URL}/++add++Device

a device 'My Device'
  Create content  type=Device  id=my-device  title=My Device


# --- WHEN -------------------------------------------------------------------

I type '${title}' into the title field
  Input Text  name=form.widgets.title  ${title}

I submit the form
  Click Button  Save

I go to the device view
  Go To  ${PLONE_URL}/my-device
  Wait until page contains  Site Map


# --- THEN -------------------------------------------------------------------

a device with the title '${title}' has been created
  Wait until page contains  Site Map
  Page should contain  ${title}
  Page should contain  Item created

I can see the device title '${title}'
  Wait until page contains  Site Map
  Page should contain  ${title}
