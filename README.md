# Pyramid Cachebust
Bust cache on static assets via query string params.

## Installation
Add to your configurator via the `include` method:

    config = Configurator()
    config.include('pyramid_cachebust')
    config.add_static_view('static', 'myapp:static')

Boom. Now you've got two new methods applied to `Request`: `cachebusted_path` and `cachebusted_url`.

    request.cachebusted_path('myapp:static/file.css')
    >>> '/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'

    request.cachebusted_url('myapp:static/file.css')
    >>> 'http://localhost/static/file.css?_=394a82fdd72eed3ac45d113bd8af554e'

The querystring gets generated in one of two ways. The default is an MD5 hexdiest of the file contents. The alternative is the file's mtime. Generation of the hash/lookup of the mtime happens once per asset. Results are cached and served upon resultant calls.

## Configuration
To place in your Pyramid `.ini`:

| name                    | type    | default   | description
|-------------------------|---------|-----------|-------------
| cachebust.enabled       | bool    | true      | toggles plugin on/off
| cachebust.reload_files  | bool    | false     | when true, cache is ignored and query param is calculated on every request
| cachebust.method        | str     | md5       | method of file calculation (md5 or mtime)
| cachebust.param_key     | str     | _         | key of query param
