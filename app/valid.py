class Validate:
    def missing_field(value, list_):
        if value not in list_:
            return jsonify({
                "message":'{} missing in data'.format(value),
                "required format":{"weight": "int","status":"string","destination":"string","pickup":"string"}
                }), 400

    def field_type(value, type_ ):
        if not type(value) == type_:
            return 'weight must be an Float!!'  