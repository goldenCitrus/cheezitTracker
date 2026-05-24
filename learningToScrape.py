import subprocess
from datetime import datetime
import json
# import asyncios
from nicegui import app, ui
from playwright.async_api import async_playwright, Page
from playwright_stealth import Stealth

    
# stock_ammount = 0.1
# Grab json file and load it into a ready state
with open('last_in_stock.json') as file:
    last_check = json.load(file)

# NAvigate to Target and grab the data we need
async def grab_info():
    # Launch browser in the background
    async with Stealth().use_async(async_playwright()) as p:
        browser = await p.chromium.launch(
            headless=True,
            # args=["--disable-blink-features=AutomationControlled"]
        )
        # Set location to Idaho Falls Target and give location permissions
        context = await browser.new_context(
            geolocation={"latitude": 43.477463, "longitude": -111.9861363},
            permissions=["geolocation"],
            # user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        # open a new page
        page: Page = await context.new_page()
        
        # item_stock_json = response_info.value.json()
        # path: ['data']['product']['fulfillment.store_options'][0]['location_available_to_promise_quantity']
        # print(item_stock_json.keys())
        
        # Here's the real meat and potatoes
        async def intercept_traffic(response):
            # Search for the right API call and grab it's response
            if "product_fulfillment_and_variation_hierarchy_v1" in response.url and "required_store_id" in response.url:
                try:
                    item_json = await response.json()
                    
                    # If it's a captcha, print a warning but KEEP LISTENING
                    if 'captchaRelativeURL' in item_json:
                        print("They're on to us...")
                    
                    # If it's the real data, grab the ammount in stock, and update the json file
                    if 'data' in item_json:
                        ammount_in_stock = item_json['data']['product']['fulfillment']['store_options'][0]['location_available_to_promise_quantity']
                        
                        last_check[0] = int(ammount_in_stock)
                        last_check[1] = f'{datetime.now().strftime('%m/%d/%Y')}, at {datetime.now().strftime("%I:%M %p")}'
                        with open("last_in_stock.json", "w") as file:
                            json.dump(last_check, file, indent=4)
                        
                        # Also print updates to the console
                        if ammount_in_stock > 0.0:
                            # ui.notify(f"Bingo. We got: {ammount_in_stock} boxes in stock")
                            print(f"Bingo. We got: {ammount_in_stock} boxes in stock")
                        elif ammount_in_stock == 0.0:
                            # ui.notify("it's joever... they're gone...")
                            print("it's joever... they're gone...")


                        return ammount_in_stock
                        # return ammount_in_stock
                # If something goes wrong, I wanna know
                except Exception as e:
                    # ui.notify(f"Wiretap hit an error: {e}")
                    print(f"Wiretap hit an error: {e}")

        # prime the grabber
        page.on("response", intercept_traffic)
        
        # Notify user, and begin animation so the user knows its activley working
        ui.notify("Navigating to Target and listening to traffic...")
        loading_overlay.set_visibility(True)
        await page.goto("https://www.target.com/p/cheez-it-gluten-free-snack-crackers-9oz/-/A-94877804")
        
        # wait for 15 seconds to get past the captcha
        await page.wait_for_timeout(5000)
        
        # close browser
        await browser.close()
        
        # Update UI
        ui.notify(f"Bingo. We got: {last_check[0]} boxes in stock")
        stock_label.set_text(f'{last_check[0]} in stock')
        last_checked_label.set_text(f'Last checked on ({last_check[1]})')
        loading_overlay.set_visibility(False)

        
# Shimmer animation
ui.add_head_html('''
<style>
  .shimmer-effect {
    position: absolute;
    inset: 0;
    background-color: rgba(25, 118, 210, 0.08); 
    overflow: hidden;
  }
  
  .shimmer-effect::before {
    content: "";
    position: absolute;
    inset: 0;
    width: 250%; 
    left: -75%;
    
    background: linear-gradient(
      135deg,
      transparent 35%,
      #61E9EEBF 50%,
      transparent 65%
    );
    
    will-change: transform;
    animation: smooth-shimmer 1.2s infinite cubic-bezier(0.4, 0.0, 0.2, 1);
  }
  
  @keyframes smooth-shimmer {
    0% {
      transform: translateX(-60%);
    }
    100% {
      transform: translateX(60%);
    }
  }
</style>
''')

# this is so there's no scroll bar
ui.query('body').classes('m-0 overflow-hidden')

# builds cheeze-it card
with ui.column().classes('w-full h-screen items-center justify-center'):    
    with ui.card().classes('items-center'):
        ui.image('cheezeit.avif').classes('w-100')
        stock_label = ui.label(f'{last_check[0]} in stock').classes('items-center')
        last_checked_label = ui.label(f'Last checked on ({last_check[1]})').classes('items-center')
        ui.button('Check Again', on_click=grab_info)
        loading_overlay = ui.element('div').classes('absolute inset-0 z-50 bg-white/30 shimmer-effect')
        loading_overlay.set_visibility(False)
            

# if __name__ == "__main__":
    # asyncio.run(grab_info())

# this is so the application opens in it's own window
@app.on_startup
def launch_app_window():
    subprocess.Popen('start msedge --app=http://127.0.0.1:8080', shell=True)

ui.run(show=False, reload=False)