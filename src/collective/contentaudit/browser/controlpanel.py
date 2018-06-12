from datetime import date
from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper
from plone.app.registry.browser.controlpanel import RegistryEditForm
from plone.z3cform import layout
from zope import schema
from zope.interface import Interface


class IContentAuditControlPanel(Interface):

    reports = schema.Text(
        title=u'Reports List',
        required=True,
        default=u'''[{"title": "Permissions", "id": "@@permission-report"},
                   {"title": "Events", "id": "@@event_manager"}]''',
    )


class ContentAuditControlPanelForm(RegistryEditForm):
    schema = IContentAuditControlPanel
    schema_prefix = "collective.contentaudit"
    label = u'Content Audit Settings'


ContentAuditControlPanelView = layout.wrap_form(
    ContentAuditControlPanelForm, ControlPanelFormWrapper)
