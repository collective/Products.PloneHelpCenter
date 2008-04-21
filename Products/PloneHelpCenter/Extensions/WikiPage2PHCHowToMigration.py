## Script (Python) "migratewiki2phc"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Migrates the How-To Wiki pages to PloneHelpCenter
##
newf = context.documentation2.howto
change_owner = context.plone_utils.changeOwnershipOf
transition = context.portal_workflow.doActionFor

def mkNiceId(id):
    """
    """
    assert(isinstance(id, str))
    newId = []
    for s in id:
        if s.isupper():
            newId.append('-'+s.lower())
        else:
            newId.append(s)
    strid = ''.join(newId)
    if strid.startswith('-'):
        strid = strid[1:]
    return strid

for old in context.documentation.howto.contentValues():
        newid=mkNiceId(old.getId())
        newf.invokeFactory('HelpCenterHowTo', newid)
        new = newf[newid]
        try:
            new.setBody(old.read())
        except:
            print "ERROR setting body for %s" % old.getId()
        new.setContentType('text/structured')
        new.setTitle(old.Title())
        new.setRelated_keywords((old.getId(),))
        try:
            change_owner(new, old.Creator(), 0)
        except:
            print "ERROR setting owner for %s" % old.getId()
        transition(new, 'submit')
        print "converted %s" % old.absolute_url()

return printed
