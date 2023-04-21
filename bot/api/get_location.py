import json

import aiohttp


async def get_location_details(lat, lon):
    url = f'https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lon}&zoom=18&addressdetails=1'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            location_data = await response.text()
            location_data = json.loads(location_data)
            address = location_data.get('address', {})
            city = address.get('city', 'Неизвестный город')
            road_name = address.get('road', 'Неизвестная дорога')
            return city, road_name

