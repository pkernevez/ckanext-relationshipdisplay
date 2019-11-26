import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
import ckan.lib.helpers as helpers

from ckan.logic import (ValidationError, NotAuthorized, NotFound, check_access)

import logging

from ckanext.relationshipdisplay import blueprint
#from ckanext.collaborators.helpers import get_collaborators
#from ckanext.collaborators.model import tables_exist
#from ckanext.collaborators.logic import action, auth

log = logging.getLogger(__name__)

class RelationshipdisplayPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    #plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.ITemplateHelpers)
    plugins.implements(plugins.IBlueprint)

    # IConfigurer

    def update_config(self, config_):
        toolkit.add_template_directory(config_, 'templates')
        toolkit.add_public_directory(config_, 'public')
        toolkit.add_resource('fanstatic', 'relationshipdisplay')
          
        
    def package_relationships(self,package_id):
      package_relationships = toolkit.get_action('package_relationships_list')(data_dict={'id': package_id})      
      return package_relationships


    def relationship_type_display(self, relation):
        return blueprint.relationship_types.get(relation,'')   
        
    def relationship_id(self, relationship):
        rel_dict =  {'object':relationship['object'], 'type':relationship['type']}
        return rel_dict
        
    def relationship_dataset(self, object_id):
        try:
            dataset = toolkit.get_action('package_show')(data_dict={'id':object_id})
        except NotAuthorized: 
            dataset = []    
        return dataset
    
    
    
    def get_helpers(self):
        return {'package_relationships': self.package_relationships, 
            'relationship_id':self.relationship_id,
            'relationship_type_display':self.relationship_type_display,
            'relationship_dataset':self.relationship_dataset,
            }
            
            
    # IBlueprint
    def get_blueprint(self):
        return blueprint.relationships