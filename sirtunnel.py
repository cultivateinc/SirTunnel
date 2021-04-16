#!/usr/bin/env python3

import sys
import json
import time
from urllib import request


if __name__ == '__main__':

    host = sys.argv[1]
    port = sys.argv[2]
    paths = sys.argv[3:]

    tunnel_id = host + '-' + port

    caddy_add_route_request = {
        "@id": tunnel_id,
        "match": [{
            "host": [host],
        }],
        "handle": [{
            "handler": "reverse_proxy",
            "upstreams":[{
                "dial": ':' + port
            }]
        }]
    }

    if len(paths) > 0:
        caddy_add_route_request["match"][0]["path"] = paths

    body = json.dumps(caddy_add_route_request).encode('utf-8')
    headers = {
        'Content-Type': 'application/json'
    }
    create_url = 'http://127.0.0.1:2019/config/apps/http/servers/sirtunnel/routes'
    req = request.Request(method='POST', url=create_url, headers=headers)
    request.urlopen(req, body)

    print("Tunnel created successfully")

    while True:
        try:
            time.sleep(1)
        except KeyboardInterrupt:

            print("Cleaning up tunnel")
            delete_url = 'http://127.0.0.1:2019/id/' + tunnel_id
            req = request.Request(method='DELETE', url=delete_url)
            request.urlopen(req)
            break
