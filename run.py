#!/usr/bin/env python3
from envoy_discovery_service import app
from envoy_discovery_service import ma  # noqa

if __name__ == '__main__':
    app.run(host="0.0.0.0")
