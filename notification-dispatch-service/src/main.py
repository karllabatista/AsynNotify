from src.interface.workers.dispatcher_notification_worker import run_worker


import asyncio
if __name__== "__main__":
   asyncio.run(run_worker())