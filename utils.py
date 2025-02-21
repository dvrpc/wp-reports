import aiohttp


async def fetch_json(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                return await response.json()
            else:
                return None


async def fetch_file(url, method="get", **options):
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, **options) as response:
            if response.status == 200:
                return await response.read()
            else:
                return None
