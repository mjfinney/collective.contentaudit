from Products.CMFCore.interfaces import IContentish
from plone.indexer.decorator import indexer

@indexer(IContentish)
def local_role_list(object, **kw):
    roles = object.get_local_roles()
    rlist = []
    for x in roles:
        if len(x[1])==1 and 'Owner' in x[1]:
            continue
        rlist.append(x[0])
    return rlist
