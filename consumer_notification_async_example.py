from typing import List
from queue import Queue
import time
import asyncio
def send_email_sync(notification)->None:

    print(f"[SYNC] Send {notification} by email...")
    time.sleep(2)
    print(f"[SYNC] notifacation-{notification} sent.")


def dispatch_notification_by_email(notifications:Queue):
    while not notifications.empty():
        notification = notifications.get()
        send_email_sync(notification)

async def send_email_async(notification)->None:

    print(f"[ASYNC] Send {notification} by email...")
    await asyncio.sleep(2)
    print(f"[ASYNC] notifacation-{notification} sent.")

async def dispatch_notification_by_email_async(notifications:asyncio.Queue):
    tasks =[]
    while not notifications.empty():
        notification = await notifications.get()
        # agendar para rodar em paralelo
        tasks.append(asyncio.create_task(send_email_async(notification)))
    # aguardar todas terminarem
    await asyncio.gather(*tasks)

async def main_async():
    notifications_async = asyncio.Queue()
    await notifications_async.put("notification-1")
    await notifications_async.put("notification-2")
    await notifications_async.put("notification-3")

    print("Executing async consumer")
    start = time.time()
    await dispatch_notification_by_email_async(notifications_async)
    end = time.time()
    print(f"Total ASYNC execution time: {end - start:.2f} seconds")
    

if __name__ == "__main__":

    notifications = Queue()
    notifications.put("notification-1")
    notifications.put("notification-2")
    notifications.put("notification-3")
    print("Executing sync consumer")
    start = time.time()
    dispatch_notification_by_email(notifications)
    end = time.time()
    print(f"Total SYNC execution time:{end-start:.2f} seconds ")

   
    # Fila assíncrona e execução
    asyncio.run(main_async())

