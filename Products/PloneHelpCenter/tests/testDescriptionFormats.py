#
# Tests for formats other than plain-text in the editing views
# 
# http://plone.org/products/plonehelpcenter/issues/99
#

import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))

from plone.app.controlpanel.markup import IMarkupSchema

from Products.PloneHelpCenter.tests import PHCTestCase


class TestDescriptionFormats(PHCTestCase.PHCTestCase):
    """
    Test that the Description field only advertises itself as
    acception text/plain
    """

    def afterSetUp(self):
        PHCTestCase.PHCTestCase.afterSetUp(self)
        
        # In the Markup Control Panel, choose more than one text
        # format from the "Alternative Formats" choices
        markup_data = IMarkupSchema(self.portal)
        markup_data.allowed_types = (
            'text/html','text/plain','text/restructured'
        )
        
        self._createFAQ(self.folder.hc.faq, 'f')
        self.faq = self.folder.hc.faq.f
        self._createHowto( getattr(self.folder.hc, 'how-to'), 'howto1' )
        self.howto = getattr(self.folder.hc, 'how-to').howto1
        self._createTutorial(self.folder.hc.tutorial, 't')
        self.tutorial = self.folder.hc.tutorial.t
        self._createLink(self.folder.hc.link, 'l')
        self.link = self.folder.hc.link.l
        self._createErrorReference(self.folder.hc.error, 'e')
        self.errorRef = self.folder.hc.error.e
        # phew, there are a lot of content types in PHC ...
    
    def testAllowableContentTypes(self):
        for obj in [
            self.faq, self.howto, self.tutorial, self.link, self.errorRef,
        ]:
            field = obj.getField('description')
            self.assertEqual(
                tuple(field.getAllowedContentTypes(obj)), ('text/plain',)
            )


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestDescriptionFormats))
    return suite

if __name__ == '__main__':
    framework()
