import asyncio
from process import MikhamImporterProcess
from config import RuntimeResource


async def main():
    resource = RuntimeResource()

    start_url = "https://mikham.me"

    mikham_importe = MikhamImporterProcess(start_url)
    await mikham_importe.start()


if __name__ == "__main__":
    # city = input("enter city name: ")
    # title = input("enter place base title: ")
    asyncio.run(main())
