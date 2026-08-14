"""Plain TCP transport for Yeelight Cube Lite matrix commands."""

from __future__ import annotations

import json
import logging
import socket
import threading

_LOGGER = logging.getLogger(__name__)
_TIMEOUT = 5


class CubeTCP:
    """Sends JSON commands to the Cube Lite over a plain TCP socket.

    Manages its own socket independently — no yeelight library involved.
    Auto-reconnects on any failure.
    """

    def __init__(self, ip: str, port: int = 55443) -> None:
        self._ip = ip
        self._port = port
        self._sock: socket.socket | None = None
        self._lock = threading.Lock()
        self._cmd_id = 0

    def send(self, method: str, params: list) -> None:
        """Send a JSON command, reconnecting once on failure."""
        with self._lock:
            self._cmd_id += 1
            payload = (
                json.dumps({"id": self._cmd_id, "method": method, "params": params})
                + "\r\n"
            ).encode()
            for attempt in range(2):
                try:
                    if self._sock is None:
                        self._sock = self._connect()
                    self._sock.sendall(payload)
                    self._sock.recv(4096)
                    return
                except Exception as exc:  # noqa: BLE001
                    _LOGGER.debug(
                        "Attempt %d for %r failed: %s — reconnecting", attempt + 1, method, exc
                    )
                    self._close()
            raise RuntimeError(f"Command {method!r} failed after reconnect")

    def close(self) -> None:
        with self._lock:
            self._close()

    def _connect(self) -> socket.socket:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(_TIMEOUT)
        sock.connect((self._ip, self._port))
        _LOGGER.debug("Connected to %s:%s", self._ip, self._port)
        return sock

    def _close(self) -> None:
        if self._sock:
            try:
                self._sock.close()
            except Exception:  # noqa: BLE001
                pass
            self._sock = None
