
import asyncio


from level2scraper.Publishers.DataStreamer import BitmexStream


b_stream = BitmexStream()
asyncio.get_event_loop().run_until_complete(b_stream.listen())

