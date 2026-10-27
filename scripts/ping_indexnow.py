import json
import re
import urllib.request

KEY = "7b9e4a2c8d1f6e3a5b0c9d8e7f6a5b4c"
HOST = "saasbill.io"
KEY_LOCATION = f"https://{HOST}/{KEY}.txt"

def main():
    with open("/workspace/saastruth/public/sitemap.xml", "r", encoding="utf-8") as f:
        xml = f.read()
    urls = re.findall(r"<loc>(https://saasbill\.io/[^<]*)</loc>", xml)
    payload = {
        "host": HOST,
        "key": KEY,
        "keyLocation": KEY_LOCATION,
        "urlList": urls,
    }
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            print(f"IndexNow ping HTTP {resp.status} for {len(urls)} URLs.")
    except urllib.error.HTTPError as e:
        print(f"IndexNow HTTP error {e.code}: {e.read().decode('utf-8', 'ignore')}")

if __name__ == "__main__":
    main()
