import os
import tempfile

from django.http import HttpResponse
from jinja2 import FileSystemLoader, Environment
from rest_framework.renderers import BaseRenderer
from rest_framework.serializers import ModelSerializer
from weasyprint import HTML, CSS
from django.conf import settings
from rest_framework import views, status
from rest_framework.request import Request
from rest_framework.response import Response
from foundry_backend.api import serializers


class BinaryFileRenderer(BaseRenderer):
    media_type = 'application/octet-stream'
    format = None
    charset = None
    render_style = 'binary'

    def render(self, data, media_type=None, renderer_context=None):
        return data


class GenerateGenericFormView(views.APIView):
    serializer: ModelSerializer
    template_name: str
    file_name: str

    renderer_classes = (BinaryFileRenderer,)

    def get_serializer(self):
        return self.serializer()

    def post(self, request: Request, **kwargs):
        """
        Generate a form from JSON key/value pairs
        """
        # Get the template
        loader = FileSystemLoader(settings.LEGAL_TEMPLATES_DIRECTORY)
        env = Environment(loader=loader)
        form_template = env.get_template(self.template_name)

        # Render the PDF
        rendered_pdf = HTML(string=form_template.render(**request.data)).write_pdf()

        # respond to the user
        response = HttpResponse(rendered_pdf, content_type='application/pdf;')
        response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(self.file_name)

        return response


class GenerateSalesContractView(GenerateGenericFormView):
    serializer = serializers.SalesContractSerializer
    template_name = 'sales_contract.html'
    file_name = 'sales_contract'


class GenerateRequestForRepairsView(GenerateGenericFormView):
    serializer = serializers.RequestForRepairsSerializer
    template_name = 'request_for_repairs.html'
    file_name = 'request_for_repairs'
