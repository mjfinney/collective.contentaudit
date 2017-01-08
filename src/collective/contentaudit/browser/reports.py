import json

from Products.Five import BrowserView
from plone import api


class ReportsMainView(BrowserView):

    def getReportList(self):
        reportlist = api.portal.get_registry_record('collective.contentaudit.reports')
        reportlist = json.loads(reportlist)
        return reportlist
