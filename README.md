# Pyramid Cachebust
Bust cache on static assets via query string params.

## Installation
Via pip:

    pip install pyramid_cachebust

## Setup
Add to your configurator via the `include` method:

    config = Configurator()
    config.include('pyramid_cachebust')
    config.add_static_view('static', 'myapp:static')

Now `pyramid.request.Request` has two new methods: `cachebusted_path` and `cachebusted_url`. These methods are wrappers for `request.static_path` and `request.static_url`, with the addition of tagging on cache-busting query parameters:

    request.cachebusted_path('myapp:static/file.css')
    >>> '/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'

    request.cachebusted_url('myapp:static/file.css')
    >>> 'http://localhost/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'

The querystring gets generated in one of two ways. The default is an MD5 hexdigest of the file contents. The two alternatives are the file's mtime ('mtime') or the time of app init ('init'). Generation of the hash/lookup of the mtime happens once per asset. Results are cached and served upon resultant calls.

## Configuration
To place in your Pyramid `.ini`:

| name                    | type    | default   | description
|-------------------------|---------|-----------|-------------
| cachebust.enabled       | bool    | true      | toggles plugin on/off
| cachebust.reload_files  | bool    | false     | when true, cache is ignored and query param is calculated on every request
| cachebust.method        | str     | md5       | method of file calculation (md5, mtime or init)
| cachebust.param_key     | str     | _         | key of query param

## Contributors
Thanks for your contributions:
* Richard Maisano (maisano)
* Marius Gedminas (mgedmin)
