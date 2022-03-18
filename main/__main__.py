import sys
from main.com.appgate.swordpish.di.configurator import Configurator
from dependency_injector.wiring import inject, Provide

from main.com.appgate.swordpish.process.url_process import UrlProcess
import logging


@inject
def main(url_process: UrlProcess = Provide[Configurator.url_process]):
    logging.info("Starting Swordphish3")
    url_process.flow().subscribe(
        on_error=lambda e: logging.error("Unexpected error: {0}".format(e)),
        on_completed=lambda: logging.error("Stream interrupted!")
    )


if __name__ == '__main__':
    container = Configurator()
    container.init_resources()
    container.wire(modules=[sys.modules[__name__]])
    main()
