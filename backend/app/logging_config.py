"""Logs on stdout, in plain text: one line per event."""

import logging
import sys

# Attributes present on every log record: anything else was passed with `extra=`.
_STANDARD_ATTRIBUTES = set(vars(logging.makeLogRecord({}))) | {
    "message",
    "asctime",
    "color_message",
}


class TextFormatter(logging.Formatter):
    """Classic text line, followed by the `extra=` fields as key=value pairs."""

    def format(self, record: logging.LogRecord) -> str:
        line = super().format(record)
        extras = " ".join(
            f"{key}={value}"
            for key, value in vars(record).items()
            if key not in _STANDARD_ATTRIBUTES
        )
        return f"{line} {extras}" if extras else line


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(TextFormatter("%(asctime)s %(levelname)s %(name)s %(message)s"))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
    # Uvicorn's own loggers go through the root handler.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True
    # Access logs are written by our middleware, with the request duration.
    logging.getLogger("uvicorn.access").disabled = True
