## Script (Python) "phc_stats_modify"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##title=Modify the selected items
##parameters=paths=[],Subject=[],Subject_mode='add',audiences=[],audiences_mode='add',sections=[],sections_mode='add',versions=[],versions_mode='add'

for p in paths:
    obj = context.restrictedTraverse(p)
    
    if Subject:
        newSubject = list(Subject)
        if Subject_mode != 'replace':
            newSubject += [s for s in obj.Subject() if s not in newSubject]
        obj.setSubject(newSubject)
        
    if audiences:
        newAudiences = list(audiences)
        if audiences_mode != 'replace':
            newAudiences += [a for a in obj.getAudiences() if a not in newAudiences]
        obj.setAudiences(newAudiences)
    
    if sections and obj.Schema().has_key('sections'):
        newSections = list(sections)
        if sections_mode != 'replace':
            newSections += [a for a in obj.getSections() if a not in newSections]
        obj.setSections(newSections)

    if versions:
        newVersions = list(versions)
        if versions_mode != 'replace':
            newVersions += [v for v in obj.getVersions() if v not in newVersions]
        obj.setVersions(newVersions)
            
    obj.reindexObject()
            

            
return state.set(status = 'success',
                 portal_status_message = 'Changes made')