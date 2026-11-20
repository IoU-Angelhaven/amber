#!/usr/bin/env python3
"""Upload the built site (dist/) to the AMBeR folder on Loopia over encrypted FTP (FTPS).

Used by .github/workflows/publish-loopia.yml. The FTP login comes from the repository secrets
FTP_USER and FTP_PASS and is never printed.

- Every file in dist/ is uploaded to public_html. Afterwards, files on the server that are no longer
  part of the site are removed, so old pages do not linger. Hidden files on the server (names that
  start with a dot, such as .well-known for the HTTPS certificate) are never touched.
- The FTP account should only reach the AMBeR folder ("Utvald underkatalog" in Loopia's Customer Zone).
  The script also works with an account that reaches the whole home directory.
- --dry-run connects and shows what would change, without changing anything.

Claude note: standard library only, so the workflow needs no third-party upload action.
"""
import argparse, ftplib, os, posixpath, ssl, sys
from pathlib import Path

HOST = "ftpcluster.loopia.se"
SITE_FOLDER = "amber.ehealth-implementation.eu"
SKIP_UPLOAD = {".nojekyll"}          # only meaningful on GitHub Pages


def connect(host, user, password, plain=False):
    if plain:                         # only for the local test, never against Loopia
        if host not in ("127.0.0.1", "localhost"):
            sys.exit("Unencrypted FTP is only allowed against this computer.")
        ftp = ftplib.FTP()
        ftp.connect(host, int(os.environ.get("FTP_PORT", "21")), timeout=60)
        ftp.login(user, password)
        return ftp
    ftp = ftplib.FTP_TLS(host, timeout=60, context=ssl.create_default_context())
    ftp.login(user, password)
    ftp.prot_p()                      # encrypt the file transfers too
    return ftp


def find_webroot(ftp):
    """public_html of the AMBeR folder, whether the account is limited to the folder or not."""
    home = ftp.pwd()
    for cand in ("public_html", f"/{SITE_FOLDER}/public_html"):
        try:
            ftp.cwd(posixpath.join(home, cand) if not cand.startswith("/") else cand)
            return ftp.pwd()
        except ftplib.error_perm:
            ftp.cwd(home)
    sys.exit("Could not find public_html for the AMBeR site with this FTP account. "
             "Check in Loopia's Customer Zone that the account is limited to the folder " + SITE_FOLDER + ".")


def listing(ftp, path):
    """[(name, is_dir)] in a remote folder."""
    try:
        return [(n, f.get("type") == "dir") for n, f in ftp.mlsd(path, facts=["type"]) if n not in (".", "..")]
    except ftplib.error_perm:
        out = []
        for full in ftp.nlst(path):
            n = posixpath.basename(full.rstrip("/"))
            if n in (".", ".."):
                continue
            here = ftp.pwd()
            try:
                ftp.cwd(posixpath.join(path, n)); out.append((n, True))
            except ftplib.error_perm:
                out.append((n, False))
            finally:
                ftp.cwd(here)
        return out


def remote_tree(ftp, root):
    """All visible files and folders under root, relative to it. Hidden names are left out."""
    files, dirs, todo = set(), set(), [""]
    while todo:
        rel = todo.pop()
        for name, is_dir in listing(ftp, posixpath.join(root, rel) if rel else root):
            if name.startswith("."):
                continue
            r = posixpath.join(rel, name) if rel else name
            if is_dir:
                dirs.add(r); todo.append(r)
            else:
                files.add(r)
    return files, dirs


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("dist", type=Path)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--host", default=HOST)
    ap.add_argument("--plain", action="store_true", help=argparse.SUPPRESS)
    a = ap.parse_args()
    if not (a.dist / "index.html").is_file():
        sys.exit(f"{a.dist} has no index.html: build the site first.")
    user, password = os.environ.get("FTP_USER", ""), os.environ.get("FTP_PASS", "")
    if not user or not password:
        sys.exit("The secrets FTP_USER and FTP_PASS are missing in the repository settings.")

    local = {p.relative_to(a.dist).as_posix() for p in a.dist.rglob("*") if p.is_file() and p.name not in SKIP_UPLOAD}
    local_dirs = {posixpath.dirname(f) for f in local} - {""}
    for d in list(local_dirs):                      # every parent folder too
        while "/" in d:
            d = posixpath.dirname(d); local_dirs.add(d)

    ftp = connect(a.host, user, password, a.plain)
    root = find_webroot(ftp)
    print(f"Signed in. The site goes to {root}")
    r_files, r_dirs = remote_tree(ftp, root)
    stale = sorted(r_files - local)
    stale_dirs = sorted(r_dirs - local_dirs, key=lambda d: -d.count("/"))
    print(f"{len(local)} files to upload ({len(local - r_files)} new). "
          f"{len(stale)} old files and {len(stale_dirs)} old folders to remove.")
    for f in stale[:50]:
        print("  remove:", f)
    if a.dry_run:
        print("Dry run: nothing was changed on the server.")
        ftp.quit(); return 0

    for d in sorted(local_dirs - r_dirs, key=lambda d: d.count("/")):
        ftp.mkd(posixpath.join(root, d))
    for i, f in enumerate(sorted(local), 1):
        with open(a.dist / f, "rb") as fh:
            ftp.storbinary("STOR " + posixpath.join(root, f), fh)
        if i % 25 == 0:
            print(f"  {i}/{len(local)} uploaded")
    for f in stale:
        ftp.delete(posixpath.join(root, f))
    for d in stale_dirs:
        try:
            ftp.rmd(posixpath.join(root, d))
        except ftplib.error_perm:
            print("  could not remove folder (not empty?):", d)
    ftp.quit()
    print(f"Done: {len(local)} files uploaded, {len(stale)} old files removed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
