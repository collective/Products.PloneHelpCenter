"""\
PloneHelpCenter tests package

To run all tests type 'python runalltests.py'
"""

# For TTW functional testing, it's nice to create some data
# that hangs around after the tests are done.  Uncomment the
# next three lines to tie some test data generation scripts
# to the portal_migration tool's Setup tab.  (Yeah, it's an
# abuse of portal_migration.  We need a portal_test_script tool.)
#
#from Products.CMFPlone import MigrationTool
#from Products.PloneHelpCenter.tests.CustomSetup import CustomSetup
#MigrationTool.registerSetupWidget(CustomSetup)
