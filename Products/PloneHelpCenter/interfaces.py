from zope.interface import Interface

class IHelpCenterContent(Interface):
    """ The HelpCenter
    """

class IHelpCenterFolder(Interface):
    """ Marker interface for PHCFolder class that is
        the ancestory of the PHC containers.
    """