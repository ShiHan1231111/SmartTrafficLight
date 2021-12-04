import asyncio


# convert to coroutine
async def reading_book():
    print("reading page 1")
    await asyncio.sleep(0)  # switch to second job
    print("reading page 2")
    await asyncio.sleep(0)
    print("reading page 3")
    await asyncio.sleep(0)
    print("reading page 4")


# convert to coroutine
async def checking_whatsapp():
    print("reading new message 1")
    await asyncio.sleep(0)  # switch to third job if have
    print("reading new message 2")
    await asyncio.sleep(0)
    print("reading new message 3")
    await asyncio.sleep(0)
    print("reading new message 4")


# convert to coroutine
async def checking_toilet():
    print("checking_toilet() 1")
    await asyncio.sleep(0)  # switch to third job if have
    print("checking_toilet() 2")
    await asyncio.sleep(0)
    print("checking_toilet() 3")
    await asyncio.sleep(0)
    print("checking_toilet() 4")


async def main():
    await asyncio.gather(*[reading_book(), checking_whatsapp(), checking_toilet()])


asyncio.run(main())
