from webargs import validate, fields as webargs_fields

PAGINATION_ARGUMENTS = {
    "limit": webargs_fields.Int(missing=100, validate=[validate.Range(min=0, max=1000)]),
    "offset": webargs_fields.Int(missing=0, validate=[validate.Range(min=0)]),
}
