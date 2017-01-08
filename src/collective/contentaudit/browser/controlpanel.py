from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IContentAuditControlPanel(Interface):

    reports = schema.Text(
        title=u'First day of the conference',
        required=True,
        default=u'[{"title": "Permissions", "id": "@@permission-report"}]',
    )


class ContentAuditControlPanelForm(RegistryEditForm):
    schema = IContentAuditControlPanel
    schema_prefix = "collective.contentaudit"
    label = u'Content Audit Settings'


ContentAuditControlPanelView = layout.wrap_form(
    ContentAuditControlPanelForm, ControlPanelFormWrapper)
