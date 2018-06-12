from plone import api
from plone.supermodel import model
from plone.directives import form
from plone.z3cform import layout
from z3c.form import button, field
from zope.interface import Interface
from zope.schema import Choice, Bool, List
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from collective.contentaudit import _

import re


class IEventManagerForm(Interface):

    model.fieldset(
        'details',
        label=_(u"Event Details"),
        fields=['creator', 'state', 'tagless', 'broken_phone','date_precedes']
    )
    creator = List(title=_(u"Creator"),
                   value_type=Choice(
                        vocabulary='plone.app.vocabularies.Users',
                       ),
                   required=False,
                   )
    state = Choice(title=_(u"Review State"),
                   values=("any", "private", "pending","published"),
                     )
    tagless = Bool(title=_(u"Events with no tags"),)
    broken_phone = Bool(title=_(u"Events with suspicious phone formats"),)
    date_precedes = Bool(title=_(u"Events where the start date precedes the creation date"),)
    model.fieldset(
        'display_options',
        label=_(u"Display Options"),
        fields=['show_creator',
                'show_state',
                'show_created',
                'show_tags',
                'show_recurring',
                'show_start',
                'show_end'
                ]
    )
    show_creator = Bool(title=_(u"Show Creator"),
                        default=True,)
    show_state = Bool(title=_(u"Show State"),
                        default=True,)
    show_created = Bool(title=_(u"Show Created Date"),
                        default=True,)
    show_tags = Bool(title=_(u"Show Tags"),
                        default=True,)
    show_recurring = Bool(title=_(u"Show If Recurring"),
                        default=True,)
    show_start = Bool(title=_(u"Show Start Dated"),
                        default=True,)
    show_end = Bool(title=_(u"Show End Dated"),
                        default=True,)

class EventManagerForm(form.Form):

    fields = field.Fields(IEventManagerForm)
    ignoreContext = True
    # Turning off CSRF allows us to share links
    # Since the forms don't have any write actions
    # this is a minimal risk.
    enableCSRFProtection = False
    method = "get"
    label = _(u"Custom Event Reports")
    data = None
    description = _(u"Use the form below to make a custom report.")

    def update(self):
        self.request.set('disable_border', True)
        super(EventManagerForm, self).update()


    #def action(self):
    #    return self.context.absolute_url() + '/@@event_manager_list'

    #def _queryBuilder(prop, query)

    @button.buttonAndHandler(_(u"Search"))
    def handleSearch(self, action):
        """{'creator': 'vmartine',
            'show_tags': True,
            'state': 'any',
            'tagless': False,
            'show_creator': True,
            'show_state': True,
            'show_recurring': True,
            'show_created': True,
            'show_start': True,
            'show_end': True}"""
        data, errors = self.extractData()
        self.data = data

        if errors:
            self.status = self.formErrorsMessage
            return

        #if data['show_creator']:


    def getEvents(self):
        cat = self.context.portal_catalog
        query = {'portal_type': "tpwd-event",}

        if self.data.get('state') in ('published', 'private', 'pending'):
            query['review_state'] = self.data['state']
        if self.data.get('creator'):
            query['Creator'] = self.data['creator']
        if self.data.get('subject'):
            query['Subject'] = subject

        results = cat(query)

        if self.data.get('tagless'):
            results = [x for x in results if x.Subject == ()]
        if self.data.get('broken_phone'):
            regex = r'\(\d{3}\) \d{3}-\d{4}( x\d+)?'
            regex = re.compile(regex)
            matches = []
            for brain in results:
                obj = brain.getObject()
                phone = obj.contact_phone

                if phone and (not regex.match(phone)):
                    matches.append(brain)
            results = matches
        if self.data.get('date_precedes'):
            lessThanStart = []
            for brain in results:
                start = brain.start
                created = brain.created
                if start<created:
                    lessThanStart.append(brain)
            results = lessThanStart
        return results


    def eventCounts(self):
        cat = self.context.portal_catalog
        events = cat(portal_type="tpwd-event")
        total = len(events)
        private, pending, published, tagless = 0, 0, 0, 0

        for e in events:
            if e.Subject == ():
                tagless += 1
            if e.review_state == 'private':
                private += 1
            if e.review_state == 'pending':
                pending += 1
            if e.review_state == 'published':
                published += 1

        return private, pending, published, tagless, total

EventManagerFormView = layout.wrap_form(EventManagerForm, index=ViewPageTemplateFile('event_manager.pt'))
