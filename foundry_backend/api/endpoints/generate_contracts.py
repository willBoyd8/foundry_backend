import os
from django.http import HttpResponse
from jinja2 import FileSystemLoader, Environment, meta
from rest_framework.renderers import BaseRenderer
from django.urls import path
from weasyprint import HTML
from django.conf import settings
from rest_framework import views, serializers
from rest_framework.request import Request


INGNORE_NAMES = ['range']


def generate_endpoint_for_legal_template(template_name: str):
    """
    Generate an api endpoint for a template
    :param template_name: The name of the template to use
    :return: an ``APIView`` object
    """
    loader = FileSystemLoader(settings.LEGAL_TEMPLATES_DIRECTORY)
    env = Environment(loader=loader)
    template_source = env.loader.get_source(env, template_name)[0]
    parsed_content = env.parse(template_source)

    fields = meta.find_undeclared_variables(parsed_content)
    template_file_name = os.path.splitext(template_name)[0]

    class GenericContractSerializer(serializers.Serializer):
        class Meta:
            ref_name = template_file_name

        def update(self, instance, validated_data):
            pass

        def create(self, validated_data):
            pass

        def get_fields(self):
            return {
                key: serializers.CharField() for key in fields if key not in INGNORE_NAMES
            }

    class BinaryFileRenderer(BaseRenderer):
        media_type = 'application/octet-stream'
        format = None
        charset = None
        render_style = 'binary'

        def render(self, data, media_type=None, renderer_context=None):
            return data

    class GenericContractView(views.APIView):
        serializer = GenericContractSerializer

        renderer_classes = (BinaryFileRenderer,)

        def get_serializer(self):
            return self.serializer()

        @staticmethod
        def post(request: Request, **_):
            """
            Generate a form from JSON key/value pairs
            """
            # Get the template
            post_loader = FileSystemLoader(settings.LEGAL_TEMPLATES_DIRECTORY)
            post_view = Environment(loader=post_loader)
            form_template = post_view.get_template(template_name)

            # Render the PDF
            rendered_pdf = HTML(string=form_template.render(**request.data)).write_pdf()

            # respond to the user
            response = HttpResponse(rendered_pdf, content_type='application/pdf;')
            response['Content-Disposition'] = 'attachment; filename={}.pdf'.format(template_file_name)

            return response

    return path(r'{}/'.format(template_file_name), GenericContractView.as_view(), name=template_file_name)


def get_all_legal_template_endpoints():
    files = os.listdir(settings.LEGAL_TEMPLATES_DIRECTORY)

    return [generate_endpoint_for_legal_template(name) for name in files]
