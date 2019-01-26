from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def api_root(request, format=None):
    """View for the root"""
    return Response("Welcome to the Logogram Application.")
