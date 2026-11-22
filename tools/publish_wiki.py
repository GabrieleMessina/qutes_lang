"""Mirror the public manual into a clean, dedicated GitHub Wiki checkout."""
import argparse
import posixpath
import re
import subprocess
from pathlib import Path
from urllib.parse import urlsplit


DOCS = Path(__file__).resolve().parents[1] / "docs"
LINK = re.compile(r"(\]\()([^()\s]+)(\))")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def render(repository):
    sources = {"README.md": "Home"}
    pages = {}
    pending = ["README.md"]
    while pending:
        source = pending.pop()

        def wiki_link(match):
            url = urlsplit(match[2])
            if url.scheme or url.netloc or not url.path:
                return match[0]
            target = posixpath.normpath(posixpath.join(posixpath.dirname(source), url.path))
            if target != "README.md" and not re.fullmatch(r"reference/[a-z0-9-]+\.md", target):
                raise ValueError(f"Unsupported local link in {source}: {match[2]}")
            if target not in sources:
                sources[target] = Path(target).stem
                pending.append(target)
            href = f"https://github.com/{repository}/wiki/{sources[target]}"
            return f"]({href}{'#' + url.fragment if url.fragment else ''})"

        lines = []
        fence = ""
        for line in (DOCS / source).read_text(encoding="utf-8").splitlines(keepends=True):
            marker = FENCE.match(line)
            if marker:
                if not fence:
                    fence = marker[1]
                elif marker[1].startswith(fence) and not line[marker.end():].strip():
                    fence = ""
            elif not fence:
                line = LINK.sub(wiki_link, line)
            lines.append(line)
        pages[sources[source] + ".md"] = "".join(lines)
    return pages


def sync(repository, checkout):
    checkout = checkout.resolve()

    def git(*args):
        return subprocess.check_output(["git", "-C", str(checkout), *args])

    origin = git("remote", "get-url", "origin").decode().strip()
    if origin != f"https://github.com/{repository}.wiki.git":
        raise ValueError("Expected a dedicated clone of the target Wiki")
    if Path(git("rev-parse", "--show-toplevel").decode().strip()).resolve() != checkout or git("status", "--porcelain"):
        raise ValueError("Expected a clean Wiki checkout root")
    pages = render(repository)
    tracked = git("ls-files", "-z").decode().split("\0")
    obsolete = [name for name in tracked if name and name not in pages]
    if obsolete:
        git("rm", "--", *obsolete)
    for name, markdown in pages.items():
        path = checkout / name
        if path.is_symlink():
            raise ValueError(f"Unexpected Wiki symlink: {name}")
        path.write_text(markdown, encoding="utf-8", newline="\n")
    git("add", "--", *pages)
    print(f"Prepared {len(pages)} Wiki pages")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repository")
    parser.add_argument("checkout", type=Path)
    args = parser.parse_args()
    sync(args.repository, args.checkout)
