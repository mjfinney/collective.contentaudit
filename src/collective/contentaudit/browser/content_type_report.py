import json
from datetime import datetime

from DateTime import DateTime
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFCore.utils import getToolByName

from plone import api
from plone.z3cform import layout

from zope.interface import Interface
from zope import schema
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form import field, form, button

items = [ ("modified", u"Modified Date"), ("Creator", u"Creator"), ("title", u"Title")]
terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]


sort_order='ascending'
class IContentTypeReportForm(Interface):
    """ Define form fields """

    portal_type = schema.Choice(
            title=u"Content Type",
            vocabulary='plone.app.vocabularies.PortalTypes',
            required=False,
        )

    path = schema.TextLine(
            title=u"Path",
            description=u"From the site root such as: /divisions/communications",
            required=False,
        )

    before_date = schema.Date(
            title=u"Show objects with modified dates before:",
            required=False,
        )

    sort_on = schema.Choice(
            title=u"Sort By",
            vocabulary=SimpleVocabulary(terms),
            required=False,
        )

    sort_order = schema.Choice(
            title=u"Sort Order",
            vocabulary=SimpleVocabulary([SimpleTerm(value="ascending",
                                                   token="ascending",
                                                   title="Ascending"),
                                        SimpleTerm(value="descending",
                                                   token="descending",
                                                   title="Descending")]),
            
            required=False,
        )

class ContentTypeReportForm(form.Form):

    fields = field.Fields(IContentTypeReportForm)
    ignoreContext = True
    # Turning off CSRF allows us to share links
    # Since the forms don't have any write actions
    # this is a minimal risk.
    enableCSRFProtection = False
    method = 'get'

    label = u"Content Type Report"
    description = u"Choose a content type from the list below"

    output = None

    @button.buttonAndHandler(u'Show Pages')
    def handleShowPages(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        query = self.formatQuery(data)

        self.output = {'pages': api.content.find(**query),
                       'path': data.get('path'),
                       'usernmae': data.get('username'),
                       }

    def formatQuery(self, data):
        query = {}
        if data.get('portal_type'):
            query['portal_type'] = data.get('portal_type')
        if data.get('path'):
            query['path'] = self.formatPath(data.get('path'))
        if data.get('before_date'):
            start = datetime.combine(data.get('before_date'), datetime.min.time())
            start = DateTime(start) # yesterday
            query['modified'] = {'query': (start),
                                'range': 'max'}
        if data.get('sort_on'):
            query['sort_on'] = data.get('sort_on')
        if data.get('sort_order'):
            query['sort_order'] = data.get('sort_order')

        return query

    def formatPath(self, path):
        if not path:
            return None
        path = path.strip('/').split('/')
        return '/'.join(self.context.getPhysicalPath() + tuple(path))


ContentTypeReportFormView = layout.wrap_form(ContentTypeReportForm, index=ViewPageTemplateFile('content_type_report.pt'))
