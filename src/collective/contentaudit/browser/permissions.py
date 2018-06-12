import json

from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone import api
from plone.batching import Batch
from plone.z3cform import layout
from Products.CMFCore.interfaces import IFolderish

from zope.interface import Interface
from zope import schema
from z3c.form import field, form, button


class IPermissionAuditForm(Interface):
    """ Define form fields """

    username = schema.Choice(
            title=u"Select User",
            description=u"If user and group are selected group will be ignored.",
            vocabulary='plone.app.vocabularies.Users',
            required=False,
        )

    groupname = schema.Choice(
            title=u"Select group",
            description=u"If user and group are selected group will be ignored.",
            vocabulary='plone.app.vocabularies.Groups',
            required=False,
        )

    path = schema.TextLine(
            title=u"Path",
            description=u"From the site root such as: /divisions/communications",
            required=False,
        )

class PermissionAuditForm(form.Form):
    """ This form can be accessed as http://yoursite/@@permission-report """

    fields = field.Fields(IPermissionAuditForm)
    ignoreContext = True
    enableCSRFProtection = True
    method = 'get'

    label = u"Permissions Audit Report"
    description = u"Select a user, group, and/or path. If user and group are selected only user will be used."

    output = None

    @button.buttonAndHandler(u'Show Pages')
    def handleShowPages(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        portal_url = api.portal.get().absolute_url()

        user_pages = None
        group_pages = None
        group_title = None
        user_fullname = None
        group_pages = []

        if data.get('username'):
            user = api.user.get(data.get('username'))
            user_fullname = user.getProperty('fullname')
            user_pages = self.getPermListForUser(data.get('username'), data.get('path'))
            groups = api.group.get_groups(username=data.get('username'))
            for group in groups:
                g = {}
                g['id'] = group.getProperty('id')
                g['title'] = group.getProperty('title')
                g['pages'] = self.getPermListForUser(g['id'], data.get('path'))
                g['link'] = portal_url + '/@@usergroup-groupmembership?groupname=' + g['id']
                group_pages.append(g)
        elif data.get('groupname'):
            g = {}
            group = api.group.get(data.get('groupname'))
            group_title = group.getProperty('title')
            g['id'] = group.getProperty('id')
            g['title'] = group_title
            g['link'] = portal_url + '/@@usergroup-groupmembership?groupname=' + g['id']
            g['pages'] = self.getPermListForUser(data.get('groupname'), data.get('path'))
            g['members'] = api.user.get_users(groupname=data.get('groupname'))
            group_pages.append(g)
        else:
            pages = self.getAllContentWithLocalPerms(data.get('path'))

        self.output = {'user_pages': user_pages,
                       'path': data.get('path'),
                       'username': data.get('username'),
                       'user_fullname': user_fullname,
                       'groupname': data.get('groupname'),
                       'group_pages': group_pages,
                       'report_h2': 'Results for ' + (user_fullname or group_title or data.get('path'))
                       }
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        #self.status = "Thank you very much!"

    def formatPath(self, path):
        if not path:
            return None
        path = path.strip('/').split('/')
        return '/'.join(self.context.getPhysicalPath() + tuple(path))

    def getAllContentWithLocalPerms(self, path=None):
        query = {'local_role_list':{'not': 'this_should_never_match'}}
        path = self.formatPath(path)
        if path:
            query['path'] = path
        return api.content.find(**query) 

    def getPermListForUser(self, user, path):
        query = {'local_role_list':user}
        path = self.formatPath(path)
        if path:
            query['path'] = path
        return api.content.find(**query) 

    def getObjectInfo(self, item):
        folderContentsLink = None
        if IFolderish.providedBy(item):
            folderContentsLink = item.absolute_url() + '/get-permissions'
        return {"title": item.title,
                "description": item.description,
                "local_roles": item.get_local_roles(),
                "url": item.absolute_url(),
                "folderContentsLink": folderContentsLink} 

    def getContents(self, item):
        contents = item.listFolderContents()
        results = []
        for i in contents:
            results.append(self.getObjectInfo(i))
        return results
    
    def getJSONContents(self, item):
        return json.dumps(self.getContents(item))

    def getRootObjects(self):
        portal = api.portal.get()
        portalContents = self.getContents(portal)
        rootInfo = self.getObjectInfo(portal)
        rootInfo['contents'] = portalContents
        return rootInfo

PermissionAuditFormView = layout.wrap_form(PermissionAuditForm, index=ViewPageTemplateFile('permissions.pt'))
