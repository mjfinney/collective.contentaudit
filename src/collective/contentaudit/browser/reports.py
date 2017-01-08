import json

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from plone import api


class ReportsMainView(BrowserView):

    def getReportList(self):
        reportlist = api.portal.get_registry_record('collective.contentaudit.reports')
        reportlist = json.loads(reportlist)
        return reportlist

    def getStatList(self):
        stats = {}
        cat = getToolByName(self.context, 'portal_catalog')
        index = cat._catalog.indexes['portal_type']
        for key in index.uniqueValues():
            t = index._index.get(key)
            if type(t) is not int:
                stats[str(key)] = len(t)
            else:
                stats[str(key)] = 1
        return stats
