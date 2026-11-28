#!/bin/bash
# Create a GitHub release and upload the bundle zip as its asset.
# Usage: push_release.sh <TOKEN>
set -e
TOKEN="$1"
ZIP=/home/z/my-project/download/grammar-engine-v9.5.0-complete.zip
API=https://api.github.com/repos/KalonixReal/randomfiles

BODY='The complete project bundle (157 files, 160.3 MB, hash-verified via BUNDLE_MANIFEST.json): the offline grammar Notepad v9.5.0, the original baseline build, the trained model delivery, all code, both dataset generations, all results including the GLM head-to-head, the report, and screenshots. Download and unzip — everything is inside.'
# shellcheck disable=SC2016
JSON=$(python3 - "$BODY" <<'PY'
import json, sys
body = sys.argv[1]
print(json.dumps({
    "tag_name": "v9.5.0-bundle",
    "target_commitish": "main",
    "name": "Grammar Engine v9.5.0 - complete bundle",
    "body": body,
    "draft": False,
    "prerelease": False,
}))
PY
)
REL=$(curl -s -X POST -H "Authorization: token $TOKEN" -H "User-Agent: bundle-uploader" -H "Content-Type: application/json" -d "$JSON" "$API/releases")
ID=$(echo "$REL" | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('id') or d)")
echo "release id: $ID"

curl -s -X POST -H "Authorization: token $TOKEN" -H "User-Agent: bundle-uploader" -H "Content-Type: application/zip" --data-binary "@$ZIP" "https://uploads.github.com/repos/KalonixReal/randomfiles/releases/$ID/assets?name=grammar-engine-v9.5.0-complete.zip" | python3 -c "import json,sys; d=json.load(sys.stdin); print('asset:', d.get('name'), d.get('size'), 'bytes,', d.get('state'), d.get('digest')); print('url:', d.get('browser_download_url'))"
