from os import stat

from time import time

from hashlib import md5

from pyramid.path import AssetResolver
from pyramid.settings import asbool


DEFAULT_CONFIG = {
    'enabled': True,
    'reload_files': False,
    'method': 'md5',
    'param_key': '_'
}


class InvalidConfig(Exception):
    pass


class CacheBust(object):
    """Class for initialized/configured with ``registry.settings``

    Serves as a callable method of ``pyramid.request.Request``

    .. code-block:: python

        cb = CacheBust(registry.settings)
        cb(request, 'myapp:path/to/static.css')
        >>> 'path/to/static.css?_=394a82fdd72eed3ac45d113bd8af554e'

    Every call to an instantiated CacheBust first looks in a local cache,
    ``self.cache`` for the filename passed in. Thusly, the cache resets
    every app reset. Of course, this can be overridden when modifying
    css and js via the ``cachebust.reload_files`` setting.

    .. code-block:: python

        cb.cache
        >>> {'myapp:path/to/static.css': '394a82fdd72eed3ac45d113bd8af554e'}

    When including :mod:`pyramid_cachebust` an instantiated CacheBust is
    added as two methods of ``pyramid.request.Request`` --
    one to wrap ``pyramid.request.Request.static_path``
    and another for ``pyramid.request.Request.static_url``:

    .. code-block:: python

        config = Configurator()
        config.include('pyramid_cachebust')
        config.add_static_view('static', 'myapp:static')

        ...

        request.cachebusted_path('myapp:static/file.css')
        >>> '/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'

        request.cachebusted_url('myapp:static/file.css')
        >>> 'http://localhost/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'
    """

    def __init__(self, settings):
        """Takes settings from app registry, builds CacheBust accordingly.
        Config options:

        `cachebust.enabled` -- defaults True

        `cachebust.reload_files` -- ignores cached hashes/mtimes

        `cachebust.param_method` -- md5, mtime, start

        `cachebust.param_key` -- query string param key

        :param settings: configurator registry settings
        :type settings: dict
        """

        settings = {
            k.replace('cachebust.', ''): v
            for k, v in settings.items()
            if k.startswith('cachebust.')
        }

        # bools
        for key in ('enabled', 'reload_files'):
            if key in settings:
                setattr(self, key, asbool(settings[key]))
            else:
                setattr(self, key, DEFAULT_CONFIG[key])

        # param_key
        pkkey = 'param_key'
        if pkkey in settings:
            setattr(self, pkkey, settings[pkkey])
        else:
            setattr(self, pkkey, DEFAULT_CONFIG[pkkey])

        # method
        pmkey = 'method'
        if pmkey in settings:
            pmval = settings[pmkey]
            if pmval not in ('md5', 'mtime', 'init'):
                raise InvalidConfig(
                    'cachebust.method must be md5, mtime, or init'
                )
            setattr(self, pmkey, pmval)
        else:
            setattr(self, pmkey, DEFAULT_CONFIG[pmkey])

        self.cache = {}
        self.init_time = int(time())

    def __call__(self, request, filename, **kwargs):
        """Returns filename via ``pyramid.request.Request.static_path``
        with query param.

        MD5, mtime, or init lookups happen once and are subsequently
        taken from ``self.cache`` dict.

        :param filename: name of file
        :type filename: str

        :return: path to static asset with query param
        :rtype: str
        """
        method = kwargs.pop('method', 'static_path')
        path = getattr(request, method)(filename, **kwargs)

        if not self.enabled:
            return path

        if filename not in self.cache or self.reload_files:
            abspath = self._get_abspath(filename)

            method_map = {
                'md5': self._get_file_hash,
                'mtime': self._get_file_mtime,
                'init': lambda _: self.init_time
            }

            self.cache[filename] = method_map[self.method](abspath)

        return '%s?%s=%s' % (
            path,
            self.param_key,
            self.cache[filename]
        )

    def _get_abspath(self, filename):
        """Get the absolute path of the file

        :param filename: name of file
        :type filename: str

        :return: abspath to file
        :rtype: str
        """
        return AssetResolver().resolve(filename).abspath()

    def _get_file_hash(self, file_loc):
        """Returns md5 hexdigest of file

        :param file_loc: path to file
        :type file_loc: str

        :return: hexdigest of file contents
        :rtype: str
        """

        fhash = md5()

        with open(file_loc, 'rb') as opened:
            while True:
                result = opened.read(1<<20)
                if not result: break
                fhash.update(result)

        return fhash.hexdigest()

    def _get_file_mtime(self, file_loc):
        """Returns mtime of file

        :param file_loc: path to file
        :type file_loc: str

        :return: stringified time of file mtime
        :rtype: str
        """

        return str(stat(file_loc).st_mtime)[:-2]
