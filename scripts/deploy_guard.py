"""Rules for the HTML GitHub Pages publishes from the root of main.

Pages is configured as legacy source branch main, path /. Generators write
public/ first. The copy at the repo root is what saasbill.io serves. These
checks refuse a placeholder homepage before that file is written or merged.
"""
import os

# Homepage must stay a full calculator, not a stub. 50 KiB is well under the
# real page (~160 KiB) and above any placeholder.
MIN_HOMEPAGE_BYTES = 50 * 1024

# Other published pages are smaller than the homepage. The shortest real page
# is about 32 KiB. 20 KiB still rejects an empty or stub file.
MIN_PAGE_BYTES = 20 * 1024

HOMEPAGE_CALCULATOR_MARKERS = (
    'id="all-calculators"',
    "editorial-workbench",
    "workbench-grid",
)


class DeployGuardError(Exception):
    pass


def check_html(html, rel_path, homepage=False):
    """Raise DeployGuardError when html must not be published."""
    if not isinstance(html, str):
        html = html.decode("utf-8", "replace")
    size = len(html.encode("utf-8"))
    if "placeholder" in html.lower():
        raise DeployGuardError("%s contains PLACEHOLDER" % rel_path)
    if homepage:
        if size < MIN_HOMEPAGE_BYTES:
            raise DeployGuardError(
                "%s is %s bytes, under the %s byte homepage minimum"
                % (rel_path, size, MIN_HOMEPAGE_BYTES)
            )
        missing = [marker for marker in HOMEPAGE_CALCULATOR_MARKERS if marker not in html]
        if missing:
            raise DeployGuardError(
                "%s is missing the calculator section: %s" % (rel_path, ", ".join(missing))
            )
        return size
    if size < MIN_PAGE_BYTES:
        raise DeployGuardError(
            "%s is %s bytes, under the %s byte page minimum"
            % (rel_path, size, MIN_PAGE_BYTES)
        )
    return size


def check_published_file(path, homepage=False):
    rel = path
    if os.path.isabs(path):
        rel = os.path.basename(path) if homepage else path
    if not os.path.isfile(path):
        raise DeployGuardError("missing published file %s" % path)
    with open(path, encoding="utf-8") as handle:
        html = handle.read()
    return check_html(html, path, homepage=homepage)
