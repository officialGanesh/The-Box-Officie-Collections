import asyncio
from requests_html import HTML
from aiohttp import ClientSession
import pandas as pd


async def fetch(url,session):
    """Returning the html content"""
    async with session.get(url) as response:
        response.raise_for_status
        html_str = await response.read()
        
        return html_str


async def main():
    """Scraping single web page"""
    
    url = "https://www.boxofficemojo.com/year/2021/"

    async with ClientSession() as session:
        
        tasks = []

        tasks.append(
            asyncio.create_task(
                fetch(url,session)
            )
        )

        page_content = await asyncio.gather(*tasks)
        
        # Saving the html (page-content) in local

        with open(f'Output/single/year{2021}.html','w') as f:
            f.write(page_content[0].decode())

        

if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    print('Code Completed 🔥')