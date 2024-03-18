import re
from data.config._version import __version__


def parse_controller_version(version):
    """Parses the controller version as described in :func:`require` into a 3-tuple
    of ([x, y, z], 'rc|a|b|dev|post', 'N') where N is the tag revision. The
    last two elements may be None.
    """
    m = re.match(
        '^([0-9]+)\\.([0-9]+)\\.([0-9]+?)(rc|a|b|\\.dev|\\.post)?([0-9]+)?$',
        version)
    if m is None:
        raise Exception('Revision format must be X.Y.Z[-tag]')

    major, minor, micro, tag, tagrev = m.groups()
    if tag == '.dev':
        tag = 'dev'
    if tag == '.post':
        tag = 'post'
    return [int(major), int(minor), int(micro)], tag, tagrev



