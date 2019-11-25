from ckan.plugins.toolkit import (request, BaseController, abort, render, c, h,
                                  _)
from ckan.logic import (ValidationError, NotAuthorized, NotFound, check_access,
                        get_action, clean_dict, tuplize_dict, parse_params)
                        
#import ckan.lib.navl.dictization_functions as dict_fns
import ckan.model as model    
    
class RelationshipController(BaseController):   

    def _redirect_to_this_controller(self, *args, **kw):
        kw['controller'] = request.environ['pylons.routes_dict']['controller']
        return h.redirect_to(*args, **kw)
 
    def show(self, dataset_id ):
                
        self.context = {'for_view': True}
        try:
            pkg = get_action('package_show')(self.context,{'id': dataset_id})
            # need this as some templates in core explicitly reference
            # c.pkg_dict
            c.pkg = pkg
            c.pkg_dict = c.pkg
            
            relationships = get_action('package_relationships_list')(None, {'id': dataset_id})

        except NotAuthorized:
            abort(403)
        except NotFound:
            abort(404)
        return render(
            'package/relationships.html',
            extra_vars={'relationships': relationships})
            
    def relationship_create(self, dataset_id ):
        context = {'model': model, 'session': model.Session, 'user': c.user}
        try:
            check_access('package_update', context, dataset_id=dataset_id )
        except NotAuthorized:
            abort(403, _('Unauthorized to create relationship %s') % '')
        try:
            c.pkg_dict = get_action('package_show')(None, {'id': dataset_id})
            
            
            # if request.method == 'POST':
                # data_dict = clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(request.params))))
                # acl = data_dict.get('id')
                # if acl is None:
                    # data = {
                        # 'object': object_id,
                        # 'type': data_dict['relationship_type']
                    # }
                    # if data_dict['organization']:
                        # group = model.Package.get(data_dict['object'])
                        # if not group:
                            # message = _(u'Dataset {pkg} does not exist.').format( pkg=data_dict['object'])
                            # raise ValidationError( {'message': message}, error_summary=message)
                        # data['auth_type'] = 'org'
                        # data['auth_id'] = group.id
                # else:
                    # data = {'id': acl, 'permission': data_dict['permission']}
                    # get_action('resource_acl_patch')(None, data)
                # self._redirect_to_this_controller(action='relationships', dataset_id=dataset_id)
            # else:
                # acl = request.params.get('id')
                # if acl:
                    # c.acl_dict = get_action('package_relationship_show')(context, { 
                        # 'subject': dataset_id
                    # })
                    # if c.acl_dict['auth_type'] == 'user':
                        # c.auth = get_action('user_show')(
                            # context, {
                                # 'id': c.acl_dict['auth_id']
                            # })
                    # else:
                        # c.auth = get_action('organization_show')(
                            # context, {
                                # 'id': c.acl_dict['auth_id']
                            # })
                    # c.acl_permission = c.acl_dict['permission']
                # else:
                    # c.acl_permission = 'None'
        except NotAuthorized:
            abort(403)
        except NotFound:
            abort(404)
        except ValidationError, e:
            h.flash_error(e.error_summary)
        return render(
            'package/relationship_add.html',
            extra_vars={
                'dataset_id': dataset_id
            })
            
    def relationship_delete(self, dataset_id, object_id, relationship_type):
        context = {'model': model, 'session': model.Session, 'user': c.user}
        try:
            if request.method == 'POST':
                get_action('package_relationship_delete')(context, {'subject':dataset_id, 'object':object_id, 'type':relationship_type})
                h.flash_notice(_('Relationship has been deleted.'))
                self._redirect_to_this_controller(
                    action='show',
                    dataset_id=dataset_id)
        except NotAuthorized:
            abort(403)
        except NotFound:
            abort(404)
