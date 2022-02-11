import json
import time


def app(environ: dict, start_response):
    data = json.dumps({
        'time': time.time(),
        'url': environ['RAW_URI']
    }).encode()

    start_response(
        "200 OK", [
            ("Content-Type", "application/json"),
            ("Content-Length", str(len(data)))
        ])

    return iter([data])
