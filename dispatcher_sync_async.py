import time
import asyncio
from typing import List

# Simula envio de email síncrono (bloqueante)
def send_email_sync(notification_id):
    print(f"[SYNC] Send email {notification_id}")
    time.sleep(2) # 2s
    print(f"[SYNC] Email {notification_id} sent")

# Dispatcher síncrono processando fila
def dispatcher_sync(notifications:List):
    for n in notifications:
        send_email_sync(n)

# Simula envio de email assíncrono (não bloqueante)
async def send_email_async(notification_id):
    print(f"[ASYNC] Enviando email {notification_id}...")
    await asyncio.sleep(2)  # demora 2 segundos
    print(f"[ASYNC] Email {notification_id} enviado.")

# Dispatcher assíncrono processando fila em paralelo
async def dispatcher_async(notifications):
    tasks = [send_email_async(n) for n in notifications]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    print("Executando dispatcher síncrono:")
    start = time.time()
    dispatcher_sync([1,2,3])
    end = time.time()

    print(f"Tempo total síncrono: {end - start:.2f} segundos\n")
    
    
    print("Executando dispatcher assíncrono:")
    start = time.time()
    asyncio.run(dispatcher_async([1,2,3]))
    end = time.time()
    print(f"Tempo total assíncrono: {end - start:.2f} segundos")