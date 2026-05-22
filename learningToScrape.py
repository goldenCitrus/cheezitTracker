from nicegui import ui, run
from playwright.sync_api import sync_playwright, Page
from playwright_stealth import Stealth

stock_ammount = 0.1

def grab_info():
    with Stealth().use_sync(sync_playwright()) as p:
        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            geolocation={"latitude": 43.477463, "longitude": -111.9861363},
            permissions=["geolocation"],
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        page: Page = context.new_page()
        
        # item_stock_json = response_info.value.json()
        # path: ['data']['product']['fulfillment.store_options'][0]['location_available_to_promise_quantity']
        # print(item_stock_json.keys())
    
        def intercept_traffic(response):
            if "product_fulfillment_and_variation_hierarchy_v1" in response.url and "required_store_id" in response.url:
                try:
                    item_json = response.json()
                    
                    # If it's a captcha, print a warning but KEEP LISTENING
                    if 'captchaRelativeURL' in item_json:
                        print("They're on to us...")
                    
                    # If it's the real data, print our stock!
                    if 'data' in item_json:
                        ammount_in_stock = item_json['data']['product']['fulfillment']['store_options'][0]['location_available_to_promise_quantity']
                        if ammount_in_stock > 0.0:
                            print(f"Bingo. We got: {ammount_in_stock} boxes in stock")
                        elif ammount_in_stock == 0.0:
                            print("it's joever... they're gone...")
                        # return ammount_in_stock
                except:
                    # If a request isn't JSON or fails, just ignore it
                    pass 

        # 2. ATTACH THE WIRETAP
        page.on("response", intercept_traffic)
        
        print("Navigating to Target and listening to traffic...")
        page.goto("https://www.target.com/p/cheez-it-gluten-free-snack-crackers-9oz/-/A-94877804")
        
        # 3. KEEP THE BROWSER OPEN
        page.wait_for_timeout(15000)
        # We force the script to wait for 15 seconds so the wiretap has time to listen 
        # to all of Target's background retries. 


        browser.close()

if __name__ == "__main__":
    grab_info()