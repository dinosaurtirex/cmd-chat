import asyncio 
import cmd_chat

async def main():
    await cmd_chat.run()

if __name__ == '__main__':
    asyncio.run(main())