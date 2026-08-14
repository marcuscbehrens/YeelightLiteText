"""Plain TCP transport for Yeelight Cube Lite matrix commands."""

from __future__ import annotations

import json
import logging
import socket
import threading

_LOGGER = logging.getLogger(__name__)
_TIMEOUT = 5       # connection timeout
_RECV_TIMEOUT = 0.3  # response read timeout — device often sends nothing for update_leds


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
                    self._sock.settimeout(_RECV_TIMEOUT)
                    try:
                        self._sock.recv(4096)
                    except socket.timeout:
                        pass  # no response is normal for update_leds
                    finally:
                        self._sock.settimeout(_TIMEOUT)
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
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 10)   # start probing after 10s idle
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 5)   # probe every 5s
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)     # drop after 3 failed probes
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
