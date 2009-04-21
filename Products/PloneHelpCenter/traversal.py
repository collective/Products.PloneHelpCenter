#!/usr/bin/env python
# encoding: utf-8
"""
traversal.py

Created by Steve McMahon on 2009-04-19.
"""

import urllib

from zope.component import adapts, getMultiAdapter
from zope.component import queryMultiAdapter
from zope.app.publisher.browser import getDefaultViewName
from zope.interface import alsoProvides
from zope.publisher.interfaces.http import IHTTPRequest
from ZPublisher.BaseRequest import DefaultPublishTraverse

from interfaces import IHelpCenterFolder, IHelpCenter

class PHCBaseTraverser(DefaultPublishTraverse):

    def publishTraverse(self, request, name):
        # intercept topic

        if name == 'topic':
            furtherPath = request['TraversalRequestNameStack']
            if furtherPath:
                # put argument in request
                request['topic'] = urllib.unquote_plus(furtherPath[0])
                # clean stack
                while furtherPath:
                    furtherPath.pop()
                # use the topic view
                view = getMultiAdapter((self.context, request), name='phc_topic')
                # return view wrapped in context
                return view.__of__(self.context)
            else:
                # bounce back
                return self.context

        return super(PHCBaseTraverser, self).publishTraverse(request, name)


class PHCTraverser(PHCBaseTraverser):
    adapts(IHelpCenter, IHTTPRequest)


class PHCFolderTraverser(PHCBaseTraverser):
    adapts(IHelpCenterFolder, IHTTPRequest)

