""" support for HelpCenter templates """

import Acquisition
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from Products.PythonScripts.standard import url_quote_plus

from Products.PloneHelpCenter.config import TOPIC_VIEW_TYPES, CACHE_MINUTES

from time import time
from plone.memoize.ram import cache


CACHE_SECONDS = 60 * CACHE_MINUTES
def _cacheKey(method, self):
    # Key on both current and last-modified times so
    # that an update of the PHC object will invalidate
    # the cache.
    context = Acquisition.aq_inner(self.context)
    if CACHE_SECONDS:
        return ( time() // CACHE_SECONDS, context.modified() )
    else:
        return time()

# note that KnowledgeBases are not included; they don't really
# fit the type-folder scheme.
subtypes_tuples = (
    ('HelpCenterKnowledgeBase','HelpCenterHowTo'),
    ('HelpCenterFAQFolder','HelpCenterFAQ'),
    ('HelpCenterHowToFolder','HelpCenterHowTo'),
    ('HelpCenterTutorialFolder','HelpCenterTutorial'),
    ('HelpCenterLinkFolder','HelpCenterLink'),
    ('HelpCenterErrorReferenceFolder','HelpCenterErrorReference'),
    ('HelpCenterGlossary','HelpCenterDefinition'),
    ('HelpCenterReferenceManualFolder','HelpCenterReferenceManual'),
    ('HelpCenterInstructionalVideoFolder','HelpCenterInstructionalVideo')
    )


# case-insensitive compare
def ncCmp(a, b):
    return cmp(a.lower(), b.lower())

# compare items by startHere and caseless title
def itemCmp(a, b):
    ash = getattr(a, 'getStartHere', False)
    bsh = getattr(b, 'getStartHere', False)
    if (ash and bsh) or (not ash and not bsh):
        return cmp(a.Title.lower(), b.Title.lower())
    elif ash:
        return -1
    else:
        return 1


class HelpCenterView(BrowserView):
    """ support for HelpCenter templates """

    def __init__(self, context, request):
        """ set up a few convenience object attributes """
        
        BrowserView.__init__(self, context, request)

        self.catalog = getToolByName(self.context, 'portal_catalog')
        self.portal_url = getToolByName(self.context, 'portal_url')()      
        self.context_path = '/'.join(self.context.getPhysicalPath())


    def subtypes(self):
        """ returns a list of major container types """
        return [t[0] for t in subtypes_tuples]
    

    def rss_subtypes(self):
        """ returns a list of doc types """
        return [t[1] for t in subtypes_tuples]
        

    def getSyndicationURL(self):
        """ returns a URL for RSS feed of help doc types """

        return self.portal_url + '/search_rss?sort_on=modified&sort_order=descending&path=' \
         + self.context_path + '&' + ('&'.join(['portal_type=%s' % s[1] for s in subtypes_tuples ]))

    
    def sections(self):
        """ subtype sections in current folder """

        context = Acquisition.aq_inner(self.context)
        
        contentFilter = {'review_state':('published', 'visible',), 'portal_type' : self.subtypes()}
        return context.getFolderContents(contentFilter=contentFilter)


    def sectionContents(self, section, limit=5):
        """ return section contents """
        
        contentFilter = {'review_state':'published','sort_on':'modified','sort_order':'reverse', 'limit' : limit}
        return section.getObject().getFolderContents(contentFilter=contentFilter);        


    @cache(_cacheKey)
    def getTopics(self):
        """Returns list of major topics and subtopics; used in helpcenter_topicview"""
        
        # major topics are those defined in the HelpCenter object.
        # returns list in the form:
        # [{title, url, subtopics}, ...]
        # subtopics are [{title, url}, ...]
        
        context = Acquisition.aq_inner(self.context)
        
        here_url  = context.absolute_url()

        # get a set of the major topics
        try:
            majorTopics = context.getSectionsVocab()
        except KeyError:
            return []
        liveSections = set( self.catalog.uniqueValuesFor('getSections') )
        
        sections = []
        currTitle = ''
        for live in majorTopics:
            if live in liveSections:
                # break into main topic, sub topic
                cs = [s.strip() for s in live.split(':')]
                main = cs[0]
                sub = ': '.join(cs[1:])
                # sub = cs[-1]
                
                if main != currTitle:
                    # append a new topic dict
                    currTitle = main
                    currSubSections = []
                    sections.append(
                     {'title':currTitle,
                      'subtopics':currSubSections, 
                      'url': here_url + '/topic/' + url_quote_plus(currTitle),
                      }
                     )
                if sub:
                    # add to the subtopics list
                    id = sub.lower().replace(' ','-')  # make HTML anchor ID
                    currSubSections.append(
                     {'title':sub,
                      'url': "%s/topic/%s#%s" % (here_url, url_quote_plus(currTitle), id)
                      }
                     )

        #sections.sort(indexCmp)        
        return sections


    @cache(_cacheKey)
    def getSectionMap(self):
        """
          returns a complex list of section dicts
          [{title:sectiontitle, subtopics:listOfSubTopics, url:urlOfSection, count:itemsInSection}, ...]
          subtopics are each lists [{title:titleOfSubSection,url:urlOfSubSection}]
          This is used in helpcenter_ploneorg.pt.
        """
        
        context = Acquisition.aq_inner(self.context)
        
        here_url  = context.absolute_url()
        phc = context.getPHCObject()
        
        topics = phc.getSectionsVocab()
        
        # dict to save counts
        topicsDict = {}
        
        for topic in topics:
            if ':' not in topic:
                items = self.catalog(portal_type=['HelpCenterReferenceManual','HelpCenterTutorial','HelpCenterHowTo'],
                                               review_state='published',
                                               getSections=[topic])
                for item in items:
                    for section in item.getSections:
                        topicsDict[section] = topicsDict.get(section, 0) + 1
        
        sections = []
        currTitle = ''
        for topic in topics:
            count = topicsDict.get(topic)
            if count:
                # break into main topic, sub topic
                cs = [s.strip() for s in topic.split(':')]
                main = cs[0]
                sub = ': '.join(cs[1:])
                
                if main != currTitle:
                    # append a new topic dict
                    currTitle = main
                    currSubSections = []
                    sections.append(
                     {'title':currTitle,
                      'subtopics':currSubSections,
                      'url': here_url + '/topic/' + url_quote_plus(currTitle),
                      'count':count
                      }
                     )
                if sub:
                    # add to the subtopics list
                    id = sub.lower().replace(' ','-')  # make HTML anchor ID
                    currSubSections.append(
                     {'title':sub,
                      'url': "%s/topic/%s#%s" % (here_url, url_quote_plus(currTitle), id)
                      }
                     )
            
        return sections


    @cache(_cacheKey)
    def getStartHeres(self, startHereLimit=10):
        """
          returns a list of topic dicts
          [{title:topicTitle, startheres:listOfStartHeres, url:urlOfTopic, count:itemsInTopic}, ...]
          startheres are dicts {title:titleOfStartHere,url:urlOfStartHere}
          This is used in helpcenter_ploneorg3.pt.
        """

        context = Acquisition.aq_inner(self.context)

        here_url  = context.absolute_url()
        phc = context.getPHCObject()

        topics = phc.getSectionsVocab()
        sections = []
        for topic in topics:
            if ':' not in topic:
                items = self.catalog(portal_type=['HelpCenterReferenceManual','HelpCenterTutorial','HelpCenterHowTo'],
                                               review_state='published',
                                               getSections=[topic])
                
                startHeres = []
                for item in items:
                    if item.getStartHere:
                        startHeres.append( {'title':item.Title, 'url':item.getURL()} )
                
                sections.append(
                 {'title':topic,
                  'startheres': startHeres[:startHereLimit],
                  'url': here_url + '/topic/' + url_quote_plus(topic),
                  'count':len(items),
                  }
                 )

        return sections


    def getSubTopics(self, topic="Visual Design", portal_types=TOPIC_VIEW_TYPES):
        """Get subtopics for phc_topic_area -- a utility for the phc_topicarea view"""
        
        context = Acquisition.aq_inner(self.context)

        # Returns sorted list of dicts in the form:
        # { 'title': title, 'id':id, 'docs': docs, }
        # docs are a sorted list of document brains

        # get a list of brains for all items of matching type and topic
        items = self.catalog(portal_type=portal_types, 
                             getSections=topic, 
                             path=context.getPHCPath())
        
        # construct a dict of subtopics under this topic
        # with a list of matching items as value
        subtopics = {}
        for item in items:
            # Add item to subtopics by section.
            # Sections should have the format "topic : subtopic"
            sections = []
            for s in item.getSections:
                if s.startswith(topic):
                    pos = s.find(':')
                    if pos > 0:
                        sections.append(s[pos+1:].strip())
            if sections:
                for s in sections:
                    subtopics.setdefault(s, []).append(item)
            else:
                subtopics.setdefault('!!!General', []).append(item)
            
        # Sort the subtopics
        keys = subtopics.keys()
        keys.sort(ncCmp)
        
        # organize into an array of dicts with keys: title, id, docs
        # where docs is a sorted list of docs in section with 'start here' docs at top
        sorted_list = []
        for k in keys:
          title = k.replace('!!!','') # strip off force-alpha
          id = title.lower().replace(' ','-')  # make HTML anchor ID
          docs = subtopics[k]
          docs.sort(itemCmp)
          sorted_list.append( { 'title': title, 'id':id, 'docs': docs, } )
        
        return sorted_list


    @cache(_cacheKey)
    def getMajorTopics(self):
        """Returns a sorted list of major sections"""

        context = Acquisition.aq_inner(self.context)

        topics = {}
        for topic in context.getSectionsVocab():
            pos = topic.find(':')
            if pos > 0:
                topics.setdefault(topic[:pos].strip(), 1)
            else:
                topics.setdefault(topic, 1)
        
        keys = topics.keys()
        keys.sort(ncCmp)
        
        return keys


    def getNonPHCContents(self):
        """Get a list of folder objects of types not defined by the help
        center product which have been placed in this help center.
        """
        
        context = Acquisition.aq_inner(self.context)

        phcTypes = context.allowed_content_types
        allTypes = self.catalog.uniqueValuesFor('portal_type')

        nonPHCTypes = [t for t in allTypes if t not in phcTypes]

        # Need this, else we end up with all types, not no types :)
        if not nonPHCTypes:
            return []

        return context.getFolderContents(contentFilter = {'portal_type' : nonPHCTypes}, batch=True)


    def statsQueryCatalog(self):
        """
            Find documentation items based on a statistics query.
            Used in phc_stats_search.cpt
        """
        
        context = Acquisition.aq_inner(self.context)

        REQUEST = context.REQUEST
        
        catalogMatches = context.queryCatalog(REQUEST=REQUEST, use_types_blacklist=False)
        matches = [m for m in catalogMatches]
        
        # Now do checks for comments, multiple sections/audiences/versions
        
        multipleSections = REQUEST.get('getSections_multiple', False)
        if multipleSections:
            matches = [m for m in matches if len(m.getSections) > 1]
            
        noSections = REQUEST.get('getSections_none', False)
        if noSections:
            matches = [m for m in matches if len(m.getSections) == 0]
            
        multipleAudiences = REQUEST.get('getAudiences_multiple', False)
        if multipleAudiences:
            matches = [m for m in matches if len(m.getAudiences) > 1]
        
        multipleVersions = REQUEST.get('getVersions_multiple', False)
        if multipleVersions:
            matches = [m for m in matches if len(m.getVersions) > 1]
            
        noVersions = REQUEST.get('getVersions_none', False)
        if noVersions:
            matches = [m for m in matches if len(m.getVersions) == 0]
            
        hasComments = REQUEST.get('hasComments', False)
        if hasComments:
            matchedPaths = [m.getPath() for m in matches]
            comments = self.catalog.searchResults(path = matchedPaths, 
                                                  portal_type = 'Discussion Item')
                                             
            foundPaths = {}
            for c in comments:
                path = c.getPath()
                idx = path.rfind('/talkback')
                path = path[:idx]
                id = path.split('/')[-1]
                foundPaths[path] = 1
                
            matches = [m for m in matches if m.getPath() in foundPaths]
                
        return matches

    def searchTypes(self):
        """
         Determine which portal_types to search
         based on the request and our type list.
        """
        
        context = Acquisition.aq_inner(self.context)

        # get our choice from the form request
        request = context.REQUEST
        choice = request.form.get("phc_selection",None)
        
        # map our sections to our eligible choices
        choiceTypes={
            "faq":('HelpCenterFAQ','HelpCenterFAQFolder'),
            "howto":("HelpCenterHowTo","HelpCenterHowtoFolder"),
            "tutorial":("HelpCenterTutorial","HelpCenterTutorialFolder", \
                        "HelpCenterLeafPage"),
            "link":("HelpCenterLink","HelpCenterLinkFolder"),
            "error":("HelpCenterErrorReference","HelpCenterErrorReferenceFolder"),
            "glossary":("HelpCenterDefinition","HelpCenterGlossary"),
            "manual":("HelpCenterReferenceManual","HelpCenterReferenceManualFolder", \
                    "HelpCenterReferenceManualSection","HelpCenterReferenceManualPage"),
            "video":("HelpCenterInstructionalVideo","HelpCenterInstructionalVideoFolder"),
        }
        
        if choice and choiceTypes.has_key(choice):
            result = choiceTypes.get(choice)
        else:
            # choice must have been "all documentation"
            result=['HelpCenterFAQ',
                    'HelpCenterHowTo',
                    'HelpCenterTutorial',
                    'HelpCenterTutorialPage',
                    'HelpCenterLink',
                    'HelpCenterErrorReference',
                    'HelpCenterDefinition',
                    'HelpCenterReferenceManual',
                    'HelpCenterReferenceManualSection',
                    'HelpCenterReferenceManualPage',
                    'HelpCenterInstructionalVideo']
        
        return result



