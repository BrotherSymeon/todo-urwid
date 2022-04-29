import logging

from clitodoapp.app.version import __version__

LOG = logging.getLogger(__name__)


def run(parser) -> None:
    LOG.info(
        "hello from clitodoapp v%s",
        __version__,
    )
