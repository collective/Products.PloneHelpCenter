# This is a zopectl run script to migrate the contents
# of content-type-specific PHC folders into conventional folders
# based on topic.

adminUser = "admin"
myPHC = 'Plone/documentation'
sources = ('how-to', 'tutorial',)
targetId = 'kb'

folderType = 'Folder'

folderIdMap ={
    'Basic Use' : 'basic-use',
    'Configuration and Set-Up' : 'config',
    'Contributing to plone.org' : 'contrib',
    'Developing for Plone' : 'developing',
    'Installation' : 'installation',
    'Internationalization and Localization' : 'i18n',
    'Managing Content' : 'managing-content',
    'Navigation' : 'navigation',
    'Upgrading and Moving' : 'upgrading',
    'Users, Authentication, and Permissions' : 'users-auth',
    'Visual Design' : 'visual-design',
}

import sys

from Testing.makerequest import makerequest

import transaction
from zope.component import queryUtility, queryMultiAdapter
from plone.i18n.normalizer.interfaces import IURLNormalizer
from Products.CMFPlone.utils import _createObjectByType

from AccessControl.SecurityManagement import \
    newSecurityManager, noSecurityManager

from Products.PloneHelpCenter.interfaces import IHelpCenterContent
from Products.PloneHelpCenter.browser.helpcenter import HelpCenterView

normalize = queryUtility(IURLNormalizer).normalize

app = makerequest(app)

acl_users = app.acl_users
user = acl_users.getUser(adminUser)
if user:
    user = user.__of__(acl_users)
    newSecurityManager(None, user)
else:
    print "Retrieving admin user failed"
    sys.exit(1)

phc = app.unrestrictedTraverse(myPHC)
print phc

phcView = HelpCenterView(phc, app.REQUEST)
print phcView

target = phc.unrestrictedTraverse(targetId)
print target

majorTopics = phcView.getMajorTopics()

# create target folders
ids = target.objectIds()
for title in majorTopics:
    id = folderIdMap.get(title, normalize(title))
    if id not in ids:
        print id, title
        _createObjectByType(folderType, target, id)
        obj = target[id]
        obj.setTitle(title)
        obj.reindexObject()
transaction.commit()

# walk the sources
for source in [phc[s] for s in sources]:
    print source
    
    for id, object in source.objectItems():
        # find the first section
        spos = 99
        pSection = ''
        for section in [section.split(':')[0] for section in object.getSections() if section]:
            mypos = majorTopics.index(section)
            if mypos < spos:
                pSection = section
                spos = mypos
        if pSection:
            fid = folderIdMap.get(pSection)
            if fid:
                folder = target[fid]
                if id not in folder.objectIds():
                    # cut and paste -- keeps publications state
                    cb = source.manage_cutObjects(id)
                    folder.manage_pasteObjects(cb)
                    folder[id].reindexObject()
                    transaction.commit()
                else:
                    print "Duplicate id: %s" % id
                    # source.manage_deleteObjects(id)
            else:
                # target folder not present -- should be an odd case
                print "No fid: %s %s" % (id, pSection,)
        else:
            # Leave it where it is
            print "No sections: ",
            print id, object.getSections()
            
noSecurityManager()
