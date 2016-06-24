from common.models import CassandraThing
from .models import AbstractPerson, BasePerson, Person, Relating, Relation

TEST_RESULTS = {
    'get_all_field_names': {
        CassandraThing: [
            'id',
            'data_abstract',
        ],
        Person: [
            'baseperson_ptr',
            'baseperson_ptr_id',
            'content_type_abstract',
            'content_type_abstract_id',
            'content_type_base',
            'content_type_base_id',
            'content_type_concrete',
            'content_type_concrete_id',
            'data_abstract',
            'data_base',
            'data_inherited',
            'data_not_concrete_abstract',
            'data_not_concrete_base',
            'data_not_concrete_inherited',
            'fk_abstract',
            'fk_abstract_id',
            'fk_base',
            'fk_base_id',
            'fk_inherited',
            'fk_inherited_id',
            'followers_abstract',
            'followers_base',
            'followers_concrete',
            'following_abstract',
            'following_base',
            'following_inherited',
            'friends_abstract',
            'friends_base',
            'friends_inherited',
            'generic_relation_abstract',
            'generic_relation_base',
            'generic_relation_concrete',
            'id',
            'm2m_abstract',
            'm2m_base',
            'm2m_inherited',
            'object_id_abstract',
            'object_id_base',
            'object_id_concrete',
            'relating_basepeople',
            'relating_baseperson',
            'relating_people',
            'relating_person',
        ],
        BasePerson: [
            'content_type_abstract',
            'content_type_abstract_id',
            'content_type_base',
            'content_type_base_id',
            'data_abstract',
            'data_base',
            'data_not_concrete_abstract',
            'data_not_concrete_base',
            'fk_abstract',
            'fk_abstract_id',
            'fk_base',
            'fk_base_id',
            'followers_abstract',
            'followers_base',
            'following_abstract',
            'following_base',
            'friends_abstract',
            'friends_base',
            'generic_relation_abstract',
            'generic_relation_base',
            'id',
            'm2m_abstract',
            'm2m_base',
            'object_id_abstract',
            'object_id_base',
            'person',
            'relating_basepeople',
            'relating_baseperson'
        ],
        AbstractPerson: [
            'content_type_abstract',
            'content_type_abstract_id',
            'data_abstract',
            'data_not_concrete_abstract',
            'fk_abstract',
            'fk_abstract_id',
            'following_abstract',
            'friends_abstract',
            'generic_relation_abstract',
            'm2m_abstract',
            'object_id_abstract',
        ],
        Relating: [
            'basepeople',
            'basepeople_hidden',
            'baseperson',
            'baseperson_hidden',
            'baseperson_hidden_id',
            'baseperson_id',
            'id',
            'people',
            'people_hidden',
            'person',
            'person_hidden',
            'person_hidden_id',
            'person_id',
            'proxyperson',
            'proxyperson_hidden',
            'proxyperson_hidden_id',
            'proxyperson_id',
        ],
    },
    'fields': {
        CassandraThing: [
            'id',
            'data_abstract',
        ],
        Person: [
            'id',
            'data_abstract',
            'fk_abstract_id',
            'data_not_concrete_abstract',
            'content_type_abstract_id',
            'object_id_abstract',
            'data_base',
            'fk_base_id',
            'data_not_concrete_base',
            'content_type_base_id',
            'object_id_base',
            'baseperson_ptr_id',
            'data_inherited',
            'fk_inherited_id',
            'data_not_concrete_inherited',
            'content_type_concrete_id',
            'object_id_concrete',
        ],
        BasePerson: [
            'id',
            'data_abstract',
            'fk_abstract_id',
            'data_not_concrete_abstract',
            'content_type_abstract_id',
            'object_id_abstract',
            'data_base',
            'fk_base_id',
            'data_not_concrete_base',
            'content_type_base_id',
            'object_id_base',
        ],
        AbstractPerson: [
            'data_abstract',
            'fk_abstract_id',
            'data_not_concrete_abstract',
            'content_type_abstract_id',
            'object_id_abstract',
        ],
        Relating: [
            'id',
            'baseperson_id',
            'baseperson_hidden_id',
            'person_id',
            'person_hidden_id',
            'proxyperson_id',
            'proxyperson_hidden_id',
        ],
    },
    'local_fields': {
        CassandraThing: [],
        Person: [
            'baseperson_ptr_id',
            'data_inherited',
            'fk_inherited_id',
            'data_not_concrete_inherited',
            'content_type_concrete_id',
            'object_id_concrete',
        ],
        BasePerson: [
            'id',
            'data_abstract',
            'fk_abstract_id',
            'data_not_concrete_abstract',
            'content_type_abstract_id',
            'object_id_abstract',
            'data_base',
            'fk_base_id',
            'data_not_concrete_base',
            'content_type_base_id',
            'object_id_base',
        ],
        AbstractPerson: [
            'data_abstract',
            'fk_abstract_id',
            'data_not_concrete_abstract',
            'content_type_abstract_id',
            'object_id_abstract',
        ],
        Relating: [
            'id',
            'baseperson_id',
            'baseperson_hidden_id',
            'person_id',
            'person_hidden_id',
            'proxyperson_id',
            'proxyperson_hidden_id',
        ],
    },
    'local_concrete_fields': {
        CassandraThing: [],
        Person: [
            'baseperson_ptr_id',
            'data_inherited',
            'fk_inherited_id',
            'content_type_concrete_id',
            'object_id_concrete',
        ],
        BasePerson: [
            'id',
            'data_abstract',
            'fk_abstract_id',
            'content_type_abstract_id',
            'object_id_abstract',
            'data_base',
            'fk_base_id',
            'content_type_base_id',
            'object_id_base',
        ],
        AbstractPerson: [
            'data_abstract',
            'fk_abstract_id',
            'content_type_abstract_id',
            'object_id_abstract',
        ],
        Relating: [
            'id',
            'baseperson_id',
            'baseperson_hidden_id',
            'person_id',
            'person_hidden_id',
            'proxyperson_id',
            'proxyperson_hidden_id',
        ],
    },
    'many_to_many': {
        CassandraThing: [],
        Person: [
            'm2m_abstract',
            'friends_abstract',
            'following_abstract',
            'm2m_base',
            'friends_base',
            'following_base',
            'm2m_inherited',
            'friends_inherited',
            'following_inherited',
        ],
        BasePerson: [
            'm2m_abstract',
            'friends_abstract',
            'following_abstract',
            'm2m_base',
            'friends_base',
            'following_base',
        ],
        AbstractPerson: [
            'm2m_abstract',
            'friends_abstract',
            'following_abstract',
        ],
        Relating: [
            'basepeople',
            'basepeople_hidden',
            'people',
            'people_hidden',
        ],
    },
    'many_to_many_with_model': {
        CassandraThing: [],
        Person: [
            BasePerson,
            BasePerson,
            BasePerson,
            BasePerson,
            BasePerson,
            BasePerson,
            None,
            None,
            None,
        ],
        BasePerson: [
            None,
            None,
            None,
            None,
            None,
            None,
        ],
        AbstractPerson: [
            None,
            None,
            None,
        ],
        Relating: [
            None,
            None,
            None,
            None,
        ],
    },
    'get_all_related_objects_with_model_legacy': {
        CassandraThing: (),
        Person: (
            ('relating_baseperson', BasePerson),
            ('relating_person', None),
        ),
        BasePerson: (
            ('person', None),
            ('relating_baseperson', None),
        ),
        Relation: (
            ('fk_abstract_rel', None),
            ('fo_abstract_rel', None),
            ('fk_base_rel', None),
            ('fo_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_hidden_local': {
        CassandraThing: (),
        Person: (
            ('+', None),
            ('_relating_people_hidden_+', None),
            ('Person_following_inherited+', None),
            ('Person_following_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_m2m_inherited+', None),
            ('Relating_people+', None),
            ('Relating_people_hidden+', None),
            ('followers_concrete', None),
            ('friends_inherited_rel_+', None),
            ('relating_people', None),
            ('relating_person', None),
        ),
        BasePerson: (
            ('+', None),
            ('_relating_basepeople_hidden_+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Relating_basepeople+', None),
            ('Relating_basepeople_hidden+', None),
            ('followers_abstract', None),
            ('followers_base', None),
            ('friends_abstract_rel_+', None),
            ('friends_base_rel_+', None),
            ('person', None),
            ('relating_basepeople', None),
            ('relating_baseperson', None),
        ),
        Relation: (
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Person_m2m_inherited+', None),
            ('fk_abstract_rel', None),
            ('fk_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_abstract_rel', None),
            ('fo_base_rel', None),
            ('fo_concrete_rel', None),
            ('m2m_abstract_rel', None),
            ('m2m_base_rel', None),
            ('m2m_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_hidden': {
        CassandraThing: (),
        Person: (
            ('+', BasePerson),
            ('+', None),
            ('_relating_basepeople_hidden_+', BasePerson),
            ('_relating_people_hidden_+', None),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_m2m_abstract+', BasePerson),
            ('BasePerson_m2m_base+', BasePerson),
            ('Person_following_inherited+', None),
            ('Person_following_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_m2m_inherited+', None),
            ('Relating_basepeople+', BasePerson),
            ('Relating_basepeople_hidden+', BasePerson),
            ('Relating_people+', None),
            ('Relating_people_hidden+', None),
            ('followers_abstract', BasePerson),
            ('followers_base', BasePerson),
            ('followers_concrete', None),
            ('friends_abstract_rel_+', BasePerson),
            ('friends_base_rel_+', BasePerson),
            ('friends_inherited_rel_+', None),
            ('relating_basepeople', BasePerson),
            ('relating_baseperson', BasePerson),
            ('relating_people', None),
            ('relating_person', None),
        ),
        BasePerson: (
            ('+', None),
            ('_relating_basepeople_hidden_+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Relating_basepeople+', None),
            ('Relating_basepeople_hidden+', None),
            ('followers_abstract', None),
            ('followers_base', None),
            ('friends_abstract_rel_+', None),
            ('friends_base_rel_+', None),
            ('person', None),
            ('relating_basepeople', None),
            ('relating_baseperson', None),
        ),
        Relation: (
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Person_m2m_inherited+', None),
            ('fk_abstract_rel', None),
            ('fk_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_abstract_rel', None),
            ('fo_base_rel', None),
            ('fo_concrete_rel', None),
            ('m2m_abstract_rel', None),
            ('m2m_base_rel', None),
            ('m2m_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_local': {
        CassandraThing: (),
        Person: (
            ('followers_concrete', None),
            ('relating_person', None),
            ('relating_people', None),
        ),
        BasePerson: (
            ('followers_abstract', None),
            ('followers_base', None),
            ('person', None),
            ('relating_baseperson', None),
            ('relating_basepeople', None),
        ),
        Relation: (
            ('fk_abstract_rel', None),
            ('fo_abstract_rel', None),
            ('fk_base_rel', None),
            ('fo_base_rel', None),
            ('m2m_abstract_rel', None),
            ('m2m_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_concrete_rel', None),
            ('m2m_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model': {
        CassandraThing: (),
        Person: (
            ('followers_abstract', BasePerson),
            ('followers_base', BasePerson),
            ('relating_baseperson', BasePerson),
            ('relating_basepeople', BasePerson),
            ('followers_concrete', None),
            ('relating_person', None),
            ('relating_people', None),
        ),
        BasePerson: (
            ('followers_abstract', None),
            ('followers_base', None),
            ('person', None),
            ('relating_baseperson', None),
            ('relating_basepeople', None),
        ),
        Relation: (
            ('fk_abstract_rel', None),
            ('fo_abstract_rel', None),
            ('fk_base_rel', None),
            ('fo_base_rel', None),
            ('m2m_abstract_rel', None),
            ('m2m_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_concrete_rel', None),
            ('m2m_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_local_legacy': {
        CassandraThing: (),
        Person: (
            ('relating_person', None),
        ),
        BasePerson: (
            ('person', None),
            ('relating_baseperson', None)
        ),
        Relation: (
            ('fk_abstract_rel', None),
            ('fo_abstract_rel', None),
            ('fk_base_rel', None),
            ('fo_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_hidden_legacy': {
        CassandraThing: (),
        BasePerson: (
            ('+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Relating_basepeople+', None),
            ('Relating_basepeople_hidden+', None),
            ('person', None),
            ('relating_baseperson', None),
        ),
        Person: (
            ('+', BasePerson),
            ('+', None),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_m2m_abstract+', BasePerson),
            ('BasePerson_m2m_base+', BasePerson),
            ('Person_following_inherited+', None),
            ('Person_following_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_m2m_inherited+', None),
            ('Relating_basepeople+', BasePerson),
            ('Relating_basepeople_hidden+', BasePerson),
            ('Relating_people+', None),
            ('Relating_people_hidden+', None),
            ('relating_baseperson', BasePerson),
            ('relating_person', None),
        ),
        Relation: (
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Person_m2m_inherited+', None),
            ('fk_abstract_rel', None),
            ('fk_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_abstract_rel', None),
            ('fo_base_rel', None),
            ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_hidden_local_legacy': {
        CassandraThing: (),
        BasePerson: (
            ('+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Relating_basepeople+', None),
            ('Relating_basepeople_hidden+', None),
            ('person', None),
            ('relating_baseperson', None),
        ),
        Person: (
            ('+', None),
            ('Person_following_inherited+', None),
            ('Person_following_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_m2m_inherited+', None),
            ('Relating_people+', None),
            ('Relating_people_hidden+', None),
            ('relating_person', None),
        ),
        Relation: (
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Person_m2m_inherited+', None),
            ('fk_abstract_rel', None),
            ('fk_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_abstract_rel', None),
            ('fo_base_rel', None),
            ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_proxy_legacy': {
        CassandraThing: (),
        BasePerson: (
            ('person', None),
            ('relating_baseperson', None),
        ),
        Person: (
            ('relating_baseperson', BasePerson),
            ('relating_person', None), ('relating_proxyperson', None),
        ),
        Relation: (
            ('fk_abstract_rel', None), ('fo_abstract_rel', None),
            ('fk_base_rel', None), ('fo_base_rel', None),
            ('fk_concrete_rel', None), ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_objects_with_model_proxy_hidden_legacy': {
        CassandraThing: (),
        BasePerson: (
            ('+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_abstract+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_following_base+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_abstract+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_friends_base+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Relating_basepeople+', None),
            ('Relating_basepeople_hidden+', None),
            ('person', None),
            ('relating_baseperson', None),
        ),
        Person: (
            ('+', BasePerson),
            ('+', None),
            ('+', None),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_abstract+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_following_base+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_abstract+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_friends_base+', BasePerson),
            ('BasePerson_m2m_abstract+', BasePerson),
            ('BasePerson_m2m_base+', BasePerson),
            ('Person_following_inherited+', None),
            ('Person_following_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_friends_inherited+', None),
            ('Person_m2m_inherited+', None),
            ('Relating_basepeople+', BasePerson),
            ('Relating_basepeople_hidden+', BasePerson),
            ('Relating_people+', None),
            ('Relating_people_hidden+', None),
            ('relating_baseperson', BasePerson),
            ('relating_person', None),
            ('relating_proxyperson', None),
        ),
        Relation: (
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('+', None),
            ('BasePerson_m2m_abstract+', None),
            ('BasePerson_m2m_base+', None),
            ('Person_m2m_inherited+', None),
            ('fk_abstract_rel', None),
            ('fk_base_rel', None),
            ('fk_concrete_rel', None),
            ('fo_abstract_rel', None),
            ('fo_base_rel', None),
            ('fo_concrete_rel', None),
        ),
    },
    'get_all_related_many_to_many_with_model_legacy': {
        CassandraThing: (),
        BasePerson: (
            ('friends_abstract_rel_+', None),
            ('followers_abstract', None),
            ('friends_base_rel_+', None),
            ('followers_base', None),
            ('relating_basepeople', None),
            ('_relating_basepeople_hidden_+', None),
        ),
        Person: (
            ('friends_abstract_rel_+', BasePerson),
            ('followers_abstract', BasePerson),
            ('friends_base_rel_+', BasePerson),
            ('followers_base', BasePerson),
            ('relating_basepeople', BasePerson),
            ('_relating_basepeople_hidden_+', BasePerson),
            ('friends_inherited_rel_+', None),
            ('followers_concrete', None),
            ('relating_people', None),
            ('_relating_people_hidden_+', None),
        ),
        Relation: (
            ('m2m_abstract_rel', None),
            ('m2m_base_rel', None),
            ('m2m_concrete_rel', None),
        ),
    },
    'get_all_related_many_to_many_local_legacy': {
        CassandraThing: [],
        BasePerson: [
            'friends_abstract_rel_+',
            'followers_abstract',
            'friends_base_rel_+',
            'followers_base',
            'relating_basepeople',
            '_relating_basepeople_hidden_+',
        ],
        Person: [
            'friends_inherited_rel_+',
            'followers_concrete',
            'relating_people',
            '_relating_people_hidden_+',
        ],
        Relation: [
            'm2m_abstract_rel',
            'm2m_base_rel',
            'm2m_concrete_rel',
        ],
    },
    'virtual_fields': {
        CassandraThing: [
            'id',
            'data_abstract'
        ],
        AbstractPerson: [
            'generic_relation_abstract',
            'content_object_abstract',
        ],
        BasePerson: [
            'generic_relation_base',
            'content_object_base',
            'generic_relation_abstract',
            'content_object_abstract',
        ],
        Person: [
            'content_object_concrete',
            'generic_relation_concrete',
            'generic_relation_base',
            'content_object_base',
            'generic_relation_abstract',
            'content_object_abstract',
        ],
    },
    'labels': {
        CassandraThing: 'common.CassandraThing',
        AbstractPerson: 'model_meta.AbstractPerson',
        BasePerson: 'model_meta.BasePerson',
        Person: 'model_meta.Person',
        Relating: 'model_meta.Relating',
    },
    'lower_labels': {
        CassandraThing: 'common.cassandrathing',
        AbstractPerson: 'model_meta.abstractperson',
        BasePerson: 'model_meta.baseperson',
        Person: 'model_meta.person',
        Relating: 'model_meta.relating',
    },
}
