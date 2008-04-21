## Script(Python) "referencemanual_getSections"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Create the list of sections to print on the single page view of a manual 
##

# Returns a list of dicts, containing:
#
#   item     : The object of the section or page
#   hasBody  : True if this item has body text(i.e. it's a page)
#   number   : The numbering of the section(e.g. "1." or "2.")
#   contents : A list of sub-sections and contained pages
#
# The list of contained pages is another list of dicts, containing:
#
#   item     : The object of the section or page
#   hasBody  : True if this item has body text(i.e. it's a page)
#   number   : The numbering of the section(e.g. "1.2." or "2.3.1")
#   depth    : The depth of the section. Second-level sections are depth 2
#

filter = {'portal_type' : ['HelpCenterReferenceManualSection',
                           'HelpCenterReferenceManualPage']}

def getSubsections(section, depth, numbering):
    """Find all pages and subsections of the given top level, traversing the
    entire tree and flattening it to a list, depth first.
    """

    # Short circuit if we hit a page(no contents)
    if not section.isPrincipiaFolderish:
        return []

    items = []
    idx = 1
    for item in section.getFolderContents(contentFilter = filter):
        sectionNumber = "%s%d." % (numbering, idx,)
        hasBody = hasattr(item, 'getBody')
        items.append({'item'    : item,
                      'hasBody' : hasBody,
                      'number'  : sectionNumber,
                      'depth'   : depth})

        # Add sub-items of this section(shortcircuits if it was a page)
        items.extend(getSubsections(item, depth + 1, sectionNumber))

        idx += 1

    return items

# Begin traversal

sections = []
idx = 1
for topLevel in context.getFolderContents(contentFilter = filter):
    sectionNumber = "%s." % (idx,)
    hasBody = hasattr(topLevel, 'getBody')
    sections.append({'item'     : topLevel,
                      'hasBody'  : hasBody,
                      'number'   : sectionNumber,
                      'contents' : getSubsections(topLevel, 2, sectionNumber)})
    idx +=1

return sections