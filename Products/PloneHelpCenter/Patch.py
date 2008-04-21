from AccessControl import ClassSecurityInfo
from Acquisition import aq_base
from DateTime import DateTime
from Acquisition import aq_inner, aq_parent, aq_base, aq_chain
from Products.Archetypes.utils import shasattr
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.interfaces.Discussions import DiscussionResponse as IDiscussionResponse
try:
    from Products.CMFCore.permissions import ReplyToItem
except ImportError:
    from Products.CMFCore.CMFCorePermissions import ReplyToItem
from Products.CMFDefault.DiscussionItem import DiscussionItem, DiscussionItemContainer
from Products.CMFDefault.DiscussionTool import DiscussionTool
from config import *

PATCH_PREFIX = '_monkey_'

__refresh_module__ = 0

def monkeyPatch(originalClass, patchingClass):
    #print 'monkeyPatch', originalClass.__name__, patchingClass.__name__
    """Monkey patch original class with attributes from new class
       (Swiped from SpeedPack -- thanks, Christian Heimes!)
    
    * Takes all attributes and methods except __doc__ and __module__ from patching class
    * Safes original attributes as _monkey_name
    * Overwrites/adds these attributes in original class
    """
    for name, newAttr in patchingClass.__dict__.items():
        # don't overwrite doc or module informations
        if name not in ('__doc__', '__module__'):
            # safe the old attribute as __monkey_name if exists
            # __dict__ doesn't show inherited attributes :/
            orig = getattr(originalClass, name, None)
            if orig:
                stored_orig_name = PATCH_PREFIX + name
                stored_orig = getattr(originalClass, stored_orig_name, None)
                # don't double-patch on refresh!
                if stored_orig is None:
                    setattr(originalClass, stored_orig_name, orig)
            # overwrite or add the new attribute
            setattr(originalClass, name, newAttr)


class PatchedDiscussionItemContainer:
    #
    #   Discussable interface
    #

    security = ClassSecurityInfo()

    security.declareProtected(ReplyToItem, 'createReply')
    def createReply( self, title, text, Creator=None ):
        """Create a reply in the proper place
        """
        container = self._container

        id = int(DateTime().timeTime())
        while self._container.get( str(id), None ) is not None:
            id = id + 1
        id = str( id )

        item = DiscussionItem( id, title=title, description=title )
        item._edit( text_format='structured-text', text=text )

        if Creator:
            item.creator = Creator

        item.__of__( self ).indexObject()

        item.setReplyTo( self._getDiscussable() )

        item.__of__(self).notifyWorkflowCreated()  # added with the patch - should be fixed in CMF 1.4.8+

        self._container[ id ] = item

        return id

class PatchedDiscussionTool:

    security = ClassSecurityInfo()

    # This patch fixes CMF collector issue 314

    def getDiscussionFor(self, content):
        """ Get DiscussionItemContainer for content, create it if necessary.
        """
        if not self.isDiscussionAllowedFor( content ):
            raise DiscussionNotAllowed

        if not IDiscussionResponse.isImplementedBy(content):
            # Discussion Items use the DiscussionItemContainer object of the
            # related content item, so talkback needs to be acquired
            talkback = getattr( aq_base(content), 'talkback', None )
            if not talkback:
                self._createDiscussionFor( content )
        return content.talkback # make sure to return fully wrapped content object

try:
    from Products.CMFCore.utils import _globals as cmfcore_globals
except ImportError:
    from Products.CMFCore import cmfcore_globals
from App.Common import package_home
from os.path import join
import zLOG

x = []
CMF_VERSION = 'Unknown'
try:
    file = join(package_home(cmfcore_globals), 'version.txt')
    CMF_VERSION = open(file, 'r').read().strip()
    version = CMF_VERSION.strip()
    if version.lower().startswith('cmf-'):
        version = version[4:]
    filtered = ''
    for v in version:
        if v in ['0','1','2','3','4','5','6','7','8','9','.']:
            filtered += v
        else:
            break
    x = [int(x) for x in filtered.split('.')]
except IOError:
    # couldnt find file, oh well
    pass
except ValueError:
    # couldnt make sense of the version number
    pass
if x <= [1,4,7]:
    zLOG.LOG('PloneHelpCenter', zLOG.INFO, 'Monkey patching CMFDefault.DiscussionItem')
    monkeyPatch(DiscussionItemContainer, PatchedDiscussionItemContainer)
    monkeyPatch(DiscussionTool, PatchedDiscussionTool)
