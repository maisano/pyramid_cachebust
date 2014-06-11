import os

from functools import partial

from pyramid_cachebust.cachebust import CacheBust


def includeme(config):
    """Set up for configurator registrations

    .. code-block:: python

        config = Configurator()
        config.include('pyramid_cachebust')

    Once called, the request object recieves two new methods,
    ``cachebusted_path`` and ``cachebusted_url``
    """

    _cachebust = CacheBust(config.registry.settings)

    cachebusted_path = partial(_cachebust, method='static_path')
    cachebusted_url = partial(_cachebust, method='static_url')

    def cb_path(request, filename, **kwargs):
        return cachebusted_path(request, filename, **kwargs)

    def cb_url(request, filename, **kwargs):
        return cachebusted_url(request, filename, **kwargs)

    config.add_request_method(cb_path, 'cachebusted_path')
    config.add_request_method(cb_url, 'cachebusted_url')
