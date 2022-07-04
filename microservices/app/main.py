import asyncio

from core.jwt_auth import has_access
from core.models.services import methods_dict
from fastapi import Depends, FastAPI
from v1.consumer import PikaClient
from v1.endpoints.endpoint import router


class App(FastAPI):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pika_client = PikaClient(self.handle_incoming_message)

    @classmethod
    def handle_incoming_message(cls, body: dict):
        methods_dict[body["method"]](body=body)


app = App()
app.include_router(router, dependencies=[Depends(has_access)])


@app.on_event("startup")
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task
