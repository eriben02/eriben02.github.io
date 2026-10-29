#!/usr/bin/env python3
"""Fetch https://saasbill.io/ after deploy and refuse a placeholder homepage.

Exit 0 when the live page is HTTP 200, larger than 50 KiB, has no PLACEHOLDER
text, and still contains the calculator section. Exit 1 otherwise.
"""
import sys
import urllib.error
import urllib.request

from deploy_guard import DeployGuardError, check_html

LIVE_URL = "https://saasbill.io/"


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": "saasbill-deploy-guard"})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.status, response.read()
    except urllib.error.HTTPError as exc:
        body = exc.read()
        return exc.code, body


def main():
    status, raw = fetch(LIVE_URL)
    if status != 200:
        print("live homepage HTTP %s from %s" % (status, LIVE_URL), file=sys.stderr)
        return 1
    html = raw.decode("utf-8", "replace")
    try:
        size = check_html(html, LIVE_URL, homepage=True)
    except DeployGuardError as exc:
        print(exc, file=sys.stderr)
        return 1
    print("live homepage ok: HTTP 200, %s bytes, calculator section present" % size)
    return 0


if __name__ == "__main__":
    sys.exit(main())
