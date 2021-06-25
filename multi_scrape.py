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
    """Scraping 10 web pages (2000-2011) """
    
    for year in range(2000,2011):

        url = f"https://www.boxofficemojo.com/year/{year}/"

        async with ClientSession() as session:
            
            tasks = []

            tasks.append(
                asyncio.create_task(
                    fetch(url,session)
                )
            )

            
            page_content = await asyncio.gather(*tasks)
            
            # Saving the html (page-content) in local

            with open(f'Output/multi/html_files/collection{year}.html','w') as f:
                f.write(page_content[0].decode())


    
        raw_data = []
    
    
        with open(f'Output/multi/html_files/collection{year}.html','r') as f:
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
        df.to_csv(f'Output/multi/csv_files/collection{year}.csv',index=False)

if __name__ == "__main__":

    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(main())

    print('Code Completed 🔥')