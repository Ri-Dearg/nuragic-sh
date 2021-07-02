"""Middleware tests."""
from __future__ import unicode_literals

from django.http import HttpRequest, HttpResponse
from django.test import TestCase

from cookies.middleware import DoNotTrackMiddleware


def request():
    """Create a request object for middleware testing."""
    req = HttpRequest()
    req.META = {
        'SERVER_NAME': 'testserver',
        'SERVER_PORT': 80,
    }
    req.path = req.path_info = "/"
    return req


def response():
    """Create a response object for middleware testing."""
    resp = HttpResponse()
    resp.status_code = 200
    resp.content = b'    '
    return resp


class DoNotTrackMiddlewareTest(TestCase):
    # pylint: disable=no-member
    """Unit tests for the DoNotTrackMiddleware."""

    def test_request_dnt(self):
        """The header "DNT: 1" sets request.DNT."""
        req = request()
        resp = response()
        req.META['HTTP_DNT'] = '1'
        DoNotTrackMiddleware(resp).process_template_response(
            req, resp)
        self.assertTrue(req.DNT)

    def test_request_dnt_off(self):
        """The header "DNT: 0" clears request.DNT."""
        req = request()
        resp = response()
        req.META['HTTP_DNT'] = '0'
        DoNotTrackMiddleware(resp).process_template_response(
            req, resp)
        self.assertFalse(req.DNT)

    def test_request_no_dnt(self):
        """If the DNT header is not present, request.DNT is false."""
        req = request()
        resp = response()
        DoNotTrackMiddleware(resp).process_template_response(
            req, resp)
        self.assertFalse(req.DNT)

    def test_response(self):
        """The Vary caching header in the response includes DNT."""
        req = request()
        resp = response()
        resp = DoNotTrackMiddleware(
            response).process_template_response(req, resp)
        self.assertEqual(resp['Vary'], 'DNT')
