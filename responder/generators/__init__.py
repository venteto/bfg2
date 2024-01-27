from . import artists, museums

GENERATORS = {
    artists.uri: artists.handler,
    museums.uri: museums.handler,
}
