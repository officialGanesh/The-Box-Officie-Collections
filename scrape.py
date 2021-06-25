import asyncio
from pandas.core import indexing
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

        tasks.append(
            asyncio.create_task(
                scrape_2021()
            )
        )

        page_content = await asyncio.gather(*tasks)
        
        # Saving the html (page-content) in local

        with open(f'Output/single/collection{2021}.html','w') as f:
            f.write(page_content[0].decode())


async def scrape_2021():
    """Scraping collections data data"""
    
    
    raw_data = []
    

    with open(f'Output/single/collection{2021}.html','r') as f:
        source = f.read()

    html = HTML(html=source)
    
    table = html.find('#table')[0]
    rows = table.find('tr')
    header = [i.text for i in rows[0].find('th')]

    
    for row in rows[1:]:

        cols = row.find('td')
        row_data = []
        for index,col in enumerate(cols):
            row_data.append(col.text)

        raw_data.append(row_data)
    
    # save data in csv

    df = pd.DataFrame(raw_data,columns=header)
    df.to_csv('Output/single/collection.csv',index=False)

if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    print('Code Completed 🔥')