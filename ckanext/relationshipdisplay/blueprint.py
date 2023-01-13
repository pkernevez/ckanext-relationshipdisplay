import logging

from flask import Blueprint
from flask.views import MethodView

from ckan.common import _, g

import ckan.plugins.toolkit as toolkit
import ckan.model as model
import ckan.lib.navl.dictization_functions as dictization_functions
import ckan.logic as logic


relationship_types = {
    'depends_on':'Depends on',
    'dependency_of':'Dependency of',
    'derives_from':'Derives from',
    'has_derivation':'Has Derivation',
    'links_to':'Links to',
    'linked_from' :'Linked from',
    'child_of': 'Child of',
    'parent_of': 'Parent of'} 

def relationships_read(dataset_id):
    context = {u'model': model, u'user': toolkit.c.user}
    data_dict = {'id': dataset_id}

    try:
        toolkit.check_access(u'package_relationships_list', context, data_dict)
        # needed to ckan_extend package/edit_base.html
        pkg_dict = toolkit.get_action('package_show')(context, data_dict)
    except toolkit.NotAuthorized:
        message = 'Unauthorized to read relationships {0}'.format(dataset_id)
        return toolkit.abort(401, toolkit._(message))
    except toolkit.ObjectNotFound:
        return toolkit.abort(404, toolkit._(u'Resource not found'))

    return toolkit.render('package/relationships.html', extra_vars={
        u'pkg_dict': pkg_dict
    })

def relationships_delete(dataset_id ):
    context = {u'model': model, u'user': toolkit.c.user}
    
    try:
    
        object = toolkit.request.params.get(u'object')
        toolkit.get_action('package_relationship_delete')(context, {
            'subject': dataset_id,
            'object': toolkit.request.params.get(u'object'),
            'type': toolkit.request.params.get(u'type')
        })
    except toolkit.NotAuthorized:
        message = u'Unauthorized to delete relationships {0}'.format(dataset_id)
        return toolkit.abort(401, toolkit._(message))
    except toolkit.ObjectNotFound as e:
        return toolkit.abort(404, toolkit._(e.message))

    toolkit.h.flash_success(toolkit._('Dataset relationship with {0} removed'.format(object)))

    return toolkit.redirect_to(u'relationships.read', dataset_id=dataset_id)


class RelationshipEditView(MethodView):
    def post(self, dataset_id):
        context = {u'model': model, u'user': toolkit.c.user}

        try:
            form_dict = logic.clean_dict(
                dictization_functions.unflatten(
                    logic.tuplize_dict(
                        logic.parse_params(toolkit.request.form))))

            data_dict = {
                'subject': dataset_id,
                'object': form_dict['object'],
                'type': form_dict['type'],
                'comment': form_dict['comment']
            }

            toolkit.get_action('package_relationship_create')(context, data_dict)

        except dictization_functions.DataError:
            return toolkit.abort(400, _(u'Integrity Error'))
        except toolkit.NotAuthorized:
            message = u'Unauthorized to edit relationships {0}'.format(dataset_id)
            return toolkit.abort(401, toolkit._(message))
        except toolkit.ObjectNotFound:
            return toolkit.abort(404, toolkit._(u'Resource not found'))
        except toolkit.ValidationError as e:
            toolkit.h.flash_error(e.error_summary)
        else:
            toolkit.h.flash_success(toolkit._('Dataset Relationship Added'))

        return toolkit.redirect_to(u'relationships.read', dataset_id=dataset_id)

    def get(self, dataset_id):
        context = {u'model': model, u'user': toolkit.c.user}
        data_dict = {'id': dataset_id}

        try:
            toolkit.check_access(u'package_relationships_list', context, data_dict)
            # needed to ckan_extend package/edit_base.html
            pkg_dict = toolkit.get_action('package_show')(context, data_dict)
        except toolkit.NotAuthorized:
            message = u'Unauthorized to read relationships {0}'.format(dataset_id)
            return toolkit.abort(401, toolkit._(message))
        except toolkit.ObjectNotFound as e:
            return toolkit.abort(404, toolkit._(u'Resource not found'))

        object = toolkit.request.params.get(u'object')
        type = toolkit.request.params.get(u'type')
        relationship_comment = ""

        if object and type:
            relationships = toolkit.get_action('package_relationships_list')(context, data_dict)
            for r in relationships:
                if r['object'] == object and r['type'] == type:
                    relationship_comment = r['comment']
            #object_dict = toolkit.get_action('package_show')(context, {'id': object})
            # Needed to reuse template

        extra_vars = {u'relationship_types': [{'text': v, 'value': k} for k, v in relationship_types.items()],
                      u'pkg_dict': pkg_dict,
                      u'object': object,
                      u'type': type,
                      u'comment': relationship_comment
                      }

        return toolkit.render('package/relationship_add.html', extra_vars)


relationships = Blueprint('relationships', __name__)

relationships.add_url_rule(
    rule=u'/dataset/relationships/<dataset_id>',
    endpoint='read',
    view_func=relationships_read, methods=['GET',]
    )

relationships.add_url_rule(
    rule=u'/dataset/relationships/<dataset_id>/new',
    view_func=RelationshipEditView.as_view('new'),
    methods=['GET', 'POST',]
    )

relationships.add_url_rule(
    rule=u'/dataset/relationships/<dataset_id>/delete',
    endpoint='delete',
    view_func=relationships_delete, methods=['POST',]
    )
    
# relationships.add_url_rule(
    # rule=u'/dataset/relationships/<dataset_id>/delete/<relationship_type>/<object_id>',
    # endpoint='delete',
    # view_func=relationships_delete, methods=['POST',]
    # )