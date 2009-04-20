from zope.interface import Interface

class IHelpCenter(Interface):
    """ The Help Center itself 
    """

class IHelpCenterFolder(Interface):
    """ Marker interface for PHCFolder class that is
        the ancestory of the PHC containers.
    """

class IHelpCenterContent(Interface):
    """ Marker interface for HelpCenter leaf content classes.
    """

class IHelpCenterHowTo(Interface):
    """ Marker interface for HelpCenterHowTo class.
    """

class IHelpCenterNavRoot(Interface):
    """ Interface for content objects
        that provide nav support for their childeren,
        like manuals.
    """

    def getTOCSelectOptions(current=None):
        pass
        
    def getAllPagesURL():
        pass


class IHelpCenterMultiPage(Interface):
    """ Marker interface for content objects
        that need nav support -- like manual pages.
    """
    