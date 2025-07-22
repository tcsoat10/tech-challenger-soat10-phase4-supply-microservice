
from src.core.containers import Container
from starlette.types import ASGIApp, Receive, Scope, Send

class IdentityMapMiddleware:
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        Container.identity_map.reset()  # Garante que uma nova instância seja criada
        await self.app(scope, receive, send)
