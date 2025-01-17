from apiflask import APIFlask


def test_openapi_blueprint(app):
    assert 'openapi' in app.blueprints
    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 5
    assert 'openapi.spec' in bp_endpoints
    assert 'openapi.swagger_ui' in bp_endpoints
    assert 'openapi.swagger_ui_oauth_redirect' in bp_endpoints
    assert 'openapi.redoc' in bp_endpoints
    assert 'openapi.static' in bp_endpoints

    app = APIFlask(__name__, spec_path=None, docs_path=None, redoc_path=None)
    assert 'openapi' not in app.blueprints


def test_spec_path(app):
    assert app.spec_path

    app = APIFlask(__name__, spec_path=None)
    assert app.spec_path is None
    assert 'openapi' in app.blueprints
    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 4
    assert 'openapi.spec' not in bp_endpoints


def test_yaml_spec():
    app = APIFlask(__name__, spec_path='/spec.yaml')
    client = app.test_client()

    rv = client.get('/spec.yaml')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'text/vnd.yaml'
    assert b'title: APIFlask' in rv.data

    app = APIFlask(__name__, spec_path='/spec.yml')
    client = app.test_client()

    rv = client.get('/spec.yml')
    assert rv.status_code == 200
    assert rv.headers['Content-Type'] == 'text/vnd.yaml'
    assert b'title: APIFlask' in rv.data


def test_docs_path(app):
    assert app.docs_path

    app = APIFlask(__name__, docs_path=None)
    assert app.docs_path is None

    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 3
    assert 'openapi.swagger_ui' not in bp_endpoints
    assert 'openapi.swagger_ui_oauth_redirect' not in bp_endpoints


def test_docs_oauth2_redirect_path(client):
    rv = client.get('/docs/oauth2-redirect')
    assert rv.status_code == 200
    assert b'<title>Swagger UI: OAuth2 Redirect</title>' in rv.data
    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'oauth2RedirectUrl: "/docs/oauth2-redirect"' in rv.data

    app = APIFlask(__name__, docs_oauth2_redirect_path='/docs/oauth2/redirect')
    rv = app.test_client().get('/docs/oauth2/redirect')
    assert rv.status_code == 200
    assert b'<title>Swagger UI: OAuth2 Redirect</title>' in rv.data
    rv = app.test_client().get('/docs')
    assert rv.status_code == 200
    assert b'oauth2RedirectUrl: "/docs/oauth2/redirect"' in rv.data

    app = APIFlask(__name__, docs_oauth2_redirect_path=None)
    assert app.docs_oauth2_redirect_path is None

    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 4
    assert 'openapi.swagger_ui' in bp_endpoints
    assert 'openapi.swagger_ui_oauth_redirect' not in bp_endpoints
    rv = app.test_client().get('/docs')
    assert rv.status_code == 200
    assert b'oauth2RedirectUrl' not in rv.data


def test_redoc_path(app):
    assert app.redoc_path

    app = APIFlask(__name__, redoc_path=None)
    assert app.redoc_path is None

    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 4
    assert 'openapi.redoc' not in bp_endpoints


def test_disable_openapi_with_enable_openapi_arg(app):
    assert app.enable_openapi

    app = APIFlask(__name__, enable_openapi=False)
    assert app.enable_openapi is False

    rules = list(app.url_map.iter_rules())
    bp_endpoints = [rule.endpoint for rule in rules if rule.endpoint.startswith('openapi')]
    assert len(bp_endpoints) == 0


def test_swagger_ui(client):
    rv = client.get('/docs')
    assert rv.status_code == 200
    assert b'swagger-ui-standalone-preset.js' in rv.data


def test_redoc(client):
    rv = client.get('/redoc')
    assert rv.status_code == 200
    assert b'redoc.standalone.js' in rv.data
