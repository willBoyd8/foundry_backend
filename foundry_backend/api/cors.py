from django.http import response


class CorsMiddleware(object):

    @staticmethod
    def process_response(**_):
        response["Access-Control-Allow-Origin"] = "*"
        return response
