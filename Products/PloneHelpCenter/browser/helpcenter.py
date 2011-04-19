""" support for HelpCenter templates """

try:
    from collections import defaultdict
except ImportError:
    # Python 2.4 compatibility
    # http://code.activestate.com/recipes/523034-emulate-collectionsdefaultdict/
    class defaultdict(dict):
        def __init__(self, default_factory=None, *a, **kw):
            if (default_factory is not None and
                not hasattr(default_factory, '__call__')):
                raise TypeError('first argument must be callable')
            dict.__init__(self, *a, **kw)
            self.default_factory = default_factory
        def __getitem__(self, key):
            try:
                return dict.__getitem__(self, key)
            except KeyError:
                return self.__missing__(key)
        def __missing__(self, key):
            if self.default_factory is None:
                raise KeyError(key)
            self[key] = value = self.default_factory()
            return value
        def __reduce__(self):
            if self.default_factory is None:
                args = tuple()
            else:
                args = self.default_factory,
            return type(self), args, None, None, self.items()
        def copy(self):
            return self.__copy__()
        def __copy__(self):
            return type(self)(self.default_factory, self)
        def __deepcopy__(self, memo):
            import copy
            return type(self)(self.default_factory,
                              copy.deepcopy(self.items()))
        def __repr__(self):
            return 'defaultdict(%s, %s)' % (self.default_factory,
                                            dict.__repr__(self))
            
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
        
        # dict to save counts and start-here items
        topicsDict = defaultdict(lambda: 0)
        featuredDict = defaultdict(list)
        
        items = self.catalog(portal_type=TOPIC_VIEW_TYPES,
                             review_state='published')
        for item in items:
            for section in item.getSections:
                topicsDict[section] = topicsDict[section] + 1
                if item.getStartHere:
                    featuredDict[section].append({
                        'title': item.Title,
                        'description': item.Description,
                        'url': item.getURL(),
                    })
        
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
                    featured = featuredDict.get(topic)
                    sections.append(
                     {'title':currTitle,
                      'subtopics':currSubSections,
                      'url': here_url + '/topic/' + url_quote_plus(currTitle),
                      'count':count,
                      'featured': featured,
                      }
                     )
                if sub:
                    # add to the subtopics list
                    id = sub.lower().replace(' ','-')  # make HTML anchor ID
                    sections[-1]['count'] += count
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
        """Get subtopics for phc_topic_area -- a utility for the phc_topicarea view.
        Returns sorted list of dicts in the form:
        { 'title': title, 'id':id, 'docs': docs, }
        docs are a sorted list of document brains.

        The subtopics are presented in the same order they're set in
        the PHC or PHCFolder. Subtopics without matching items have an
        empty list under the 'docs' key.
        """

        context = Acquisition.aq_inner(self.context)

        # get a list of brains for all items of matching type and topic
        items = self.catalog(portal_type=portal_types, 
                             getSections=topic, 
                             path=context.getPHCPath())

        def isSubTopicOf(subtopic, topic):
            """Return true if the given subtopic is really a subtopic
            of topic."""
            if subtopic.startswith(topic) and subtopic!=topic \
                   and ':' in subtopic:
                return True
            return False

        subtopics = [s for s in context.getSectionsVocab() if isSubTopicOf(s, topic)]
        # place each item under the right subtopic
        subtopic_items = {}
        for item in items:
            for section in item.getSections:
                if section in subtopics:
                    subtopic_items.setdefault(section, []).append(item)
                else: # item matches the main topic but not any subtopic
                    subtopic_items.setdefault('General', []).append(item)

        sorted_list = []
        for subtopic in subtopics:
           title = subtopic[subtopic.index(':')+1:].strip()
           id = title.lower().replace(' ','-')  # make HTML anchor ID
           if subtopic in subtopic_items:
               docs = subtopic_items[subtopic]
           else:  # no docs matching this subtopic
               docs = []
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



