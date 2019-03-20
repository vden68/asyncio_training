import time
import asyncio

async def main():
    print(f'{time.ctime()} Hello!')
    await asyncio.sleep(1.0)
    print(f'{time.ctime()} Goodbye!')
    loop.stop() # (5)

loop = asyncio.get_event_loop() #(1)
loop.create_task(main()) #(2)
loop.run_forever() #(3)
pending = asyncio.Task.all_tasks(loop=loop)
group = asyncio.gather(*pending, return_exceptions=True) #(4)
loop.run_until_complete(group) #(3)
loop.close() #(5)

