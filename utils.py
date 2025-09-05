import aiohttp


async def fetch_json(url, **options):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, allow_redirects=True, **options) as response:
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
