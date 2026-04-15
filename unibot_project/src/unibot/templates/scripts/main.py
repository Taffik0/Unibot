import asyncio

from ..bot_orchestration.orchestration.main_orchestration import orchestration, start, stop, register

# ------------------------------
# Run Bot
# ------------------------------

"""
To run change directory (cd) to bot dir and use `python src/main.py` or `python -m src.main`
"""


async def main():
    bot_package = await orchestration()
    await register(bot_package)
    print("starting bot...")
    await start(bot_package)
    print("bot started")

    try:
        while True:
            await asyncio.sleep(3600)
    except (KeyboardInterrupt, asyncio.CancelledError):
        print("stopping bot...")
        await stop(bot_package)
        print("bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
