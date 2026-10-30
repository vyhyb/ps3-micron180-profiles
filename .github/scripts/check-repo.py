#!/usr/bin/env python3
"""Sanity checks for the profile repository before it is released.

- every vendor version folder has a manifest.json whose hashes match the files
- vendor.yaml `version:` matches its folder name
- vendor_indices.zip contains <Vendor>.idx whose newest entry is the newest folder

Usage: check-repo.py <repository dir> [tag]
With a tag like v1.0.2, also warns if it does not match the newest vendor version.
"""
import hashlib
import json
import os
import re
import sys
import zipfile

repo = sys.argv[1]
tag = sys.argv[2] if len(sys.argv) > 2 else None
errors = []

def vkey(v):
    return tuple(int(x) for x in v.split("."))

with zipfile.ZipFile(os.path.join(repo, "vendor_indices.zip")) as z:
    indices = {os.path.splitext(n)[0]: z.read(n).decode() for n in z.namelist() if n.endswith(".idx")}

for vendor in sorted(d for d in os.listdir(repo) if os.path.isdir(os.path.join(repo, d))):
    versions = sorted((v for v in os.listdir(os.path.join(repo, vendor)) if re.fullmatch(r"\d+(\.\d+)+", v)), key=vkey)
    for version in versions:
        vdir = os.path.join(repo, vendor, version)
        manifest = {e["filename"]: e["filehash"] for e in json.load(open(os.path.join(vdir, "manifest.json")))}
        files = {os.path.relpath(os.path.join(r, f), vdir).replace(os.sep, "/")
                 for r, _, fs in os.walk(vdir) for f in fs if f != "manifest.json"}
        for f in sorted(files - set(manifest)):
            errors.append(f"{vendor}/{version}: {f} is missing from manifest.json")
        for f in sorted(set(manifest) - files):
            errors.append(f"{vendor}/{version}: manifest.json lists missing file {f}")
        for f in sorted(files & set(manifest)):
            h = hashlib.sha256(open(os.path.join(vdir, f), "rb").read()).hexdigest()
            if h != manifest[f]:
                errors.append(f"{vendor}/{version}: hash mismatch for {f} (regenerate manifest.json)")
        m = re.search(r"^version:\s*(\S+)", open(os.path.join(vdir, "vendor.yaml")).read(), re.M)
        if not m or m.group(1) != version:
            errors.append(f"{vendor}/{version}: vendor.yaml version is {m and m.group(1)}, expected {version}")

    newest = versions[-1]
    idx = indices.get(vendor)
    if idx is None:
        errors.append(f"vendor_indices.zip has no {vendor}.idx")
    else:
        entries = [l.split()[0] for l in idx.splitlines() if re.match(r"^\d+(\.\d+)+\s", l)]
        if not entries or entries[0] != newest:
            errors.append(f"{vendor}.idx newest entry is {entries[0] if entries else None}, expected {newest}")
    if tag and tag.lstrip("v") != newest:
        print(f"::warning::tag {tag} does not match newest {vendor} version {newest}")
    print(f"{vendor}: versions {', '.join(versions)}")

if errors:
    for e in errors:
        print(f"::error::{e}")
    sys.exit(1)
print("repository OK")
