from common.models import CassandraThing

TEST_RESULTS = {
    "get_all_field_names": {
        CassandraThing: [
            "id",
            "data_abstract",
        ],
    },
    "fields": {
        CassandraThing: [
            "id",
            "data_abstract",
        ],
    },
    "local_fields": {
        CassandraThing: [],
    },
    "local_concrete_fields": {
        CassandraThing: [],
    },
    "many_to_many": {
        CassandraThing: [],
    },
    "many_to_many_with_model": {
        CassandraThing: [],
    },
    "get_all_related_objects_with_model_legacy": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_hidden_local": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_hidden": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_local": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_local_legacy": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_hidden_legacy": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_hidden_local_legacy": {
        CassandraThing: (),
    },
    "get_all_related_objects_with_model_proxy_hidden_legacy": {
        CassandraThing: (),
    },
    "get_all_related_many_to_many_with_model_legacy": {
        CassandraThing: (),
    },
    "private_fields": {
        CassandraThing: ["id", "data_abstract"],
    },
    "labels": {
        CassandraThing: "common.CassandraThing",
    },
    "lower_labels": {
        CassandraThing: "common.cassandrathing",
    },
}
