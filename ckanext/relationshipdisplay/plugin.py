import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

from ckan.logic import (ValidationError, NotAuthorized, NotFound, check_access)


class RelationshipdisplayPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'relationshipdisplay')
        
        
    # IRoutes

    def before_map(self, m):
        m.connect(
            'relationships',
            '/dataset/{dataset_id}/relationships',
            controller='ckanext.relationshipdisplay.controller:RelationshipController',
            action='show',
            ckan_icon='connectdevelop')
        m.connect(
            'relationship_create',
            '/dataset/{dataset_id}/relationship_create',
            controller='ckanext.relationshipdisplay.controller:RelationshipController',
            action='relationship_create')
        m.connect(
            'relationship_delete',
            '/dataset/{dataset_id}/relationship_delete',
            controller='ckanext.relationshipdisplay.controller:RelationshipController',
            action='relationship_delete')
        # m.connect(
            # 'relationship_delete',
            # '/dataset/{dataset_id}/relationship_delete/{relationship_type}/{object_id}',
            # controller='ckanext.relationshipdisplay.controller:RelationshipController',
            # action='relationship_delete')
        return m    
        
    def package_relationships(self,package_id):

      package_relationships = toolkit.get_action('package_relationships_list')(
          data_dict={'id': package_id})
      
      return package_relationships


    def relationship_display(self, relation):
        return relation.replace('_',' ').title()         
        
    def relationship_dataset(self, object_id):
        try:
            dataset = toolkit.get_action('package_show')(data_dict={'id':object_id})
        except NotAuthorized: 
            dataset = []    
        return dataset
    
    def get_helpers(self):
        return {'package_relationships': self.package_relationships, 
            'relationship_display':self.relationship_display,
            'relationship_dataset':self.relationship_dataset}