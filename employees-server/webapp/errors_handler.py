from webargs.flaskparser import parser


class ParametersError(Exception):
    pass


class ExternalUrlError(Exception):
    pass


def configure_error_handling(api):
    @parser.error_handler
    def handle_request_parsing_error(error, req, schema, *, error_status_code, error_headers):
        raise ParametersError(error.messages)

    def handle_error(exception, code):
        return {"message": str(exception)}, code

    @api.errorhandler(ParametersError)
    def handle_parameters_error(exception):
        return handle_error(exception, 400)

    @api.errorhandler(FileNotFoundError)
    def handle_external_url_error(exception):
        return handle_error(exception, 500)

    @api.errorhandler(ExternalUrlError)
    def handle_external_url_error(exception):
        return handle_error(exception, 502)
