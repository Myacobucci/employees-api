from webargs import validate, fields as webargs_fields

PAGINATION_ARGUMENTS = {
    "limit": webargs_fields.Int(missing=100, validate=[validate.Range(min=0, max=1000)]),
    "offset": webargs_fields.Int(missing=0, validate=[validate.Range(min=0)]),
}

DOC_PAGINATION_ARGUMENTS = {
    "limit": {"description": "Number of results. Max value: 1000.", "default": 100, "type": "integer"},
    "offset": {"description": "Offset", "default": 0, "type": "integer"},
}
