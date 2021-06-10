import asyncio


async def main():
    print("hello")
    await foo()  # blocked and wait for foo to finish
    print("world")


async def main2():
    print("hello")
    # register into event loop
    task1 = asyncio.create_task(foo())
    task2 = asyncio.create_task(bar())
    # task1 and task2 would be execute concurrently, not in order depends on which one is waiting
    await task1
    await task2
    print("world")


async def foo():
    print("foo start")
    await asyncio.sleep(5)
    print("foo end")


async def bar():
    for i in range(1, 10):
        print(i)


if __name__ == "__main__":
    asyncio.run(main2())
