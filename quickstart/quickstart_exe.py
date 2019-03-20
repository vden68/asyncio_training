import time
import asyncio

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    loop.stop()

def blocking(): #(1)
    time.sleep(0.5) #(2)
    print(f"{time.ctime()} Hello from a thread!")

loop = asyncio.get_event_loop()

loop.create_task(main())
loop.run_in_executor(None, blocking) #(3)

loop.run_forever()

pending = asyncio.Task.all_tasks(loop=loop) #(4)
group = asyncio.gather(*pending)
loop.run_until_complete(group)
loop.close()