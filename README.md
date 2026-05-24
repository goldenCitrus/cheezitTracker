# Gluten Free Cheeze-It Tracker

A Python-based desktop application designed to track the inventory of Gluten-Free Cheez-Its at Target stores. It uses NiceGUI for the frontend and Playwright to scrape Target's API in the background.

## Instructions for Build and Use

Steps to build and/or run the software:

1. Ensure Python is installed (built and tested on Python 3.14).
2. Install the required dependencies by running in the terminal: `pip install nicegui playwright playwright-stealth`.
3. Run `playwright install` in the terminal to download the necessary headless browser binaries.
4. Ensure the image file (`cheezeit.avif`) and the database file (`last_in_stock.json`) are located in the same directory as the Python script.

Instructions for using the software:

1. Run the script using `python script_name.py`.
2. The application will automatically launch a dedicated Microsoft Edge window.
3. Click the "Check Again" button to initiate the scraper. A loading animation will appear while the background process runs.
4. Wait approximately 5 seconds for the UI to update with the current inventory count and time checked.

## Development Environment

To recreate the development environment, you need the following software and/or libraries:

* Python 3.14
* NiceGUI
* Playwright & Playwright-Stealth
* Microsoft Edge

## Useful Websites to Learn More

I found these websites useful in developing this software:

* [NiceGUI Official Documentation](https://nicegui.io/documentation)
* [Playwright Documentation](https://devdocs.io/playwright-getting-started/)
* [YouTube: NiceGUI](https://www.youtube.com/watch?v=gyscrrS4hEA)
* Gemini AI

## Future Work

The following items I plan to fix, improve, and/or add to this project in the future:

* [ ] Update the script to instantly close the browser and update the UI as soon as the data is retrieved, rather than using a static 5-second wait.
* [ ] Add the ability for the user to input and track other store items.
* [ ] Add a feature allowing the user to choose their specific store location (currently hardcoded to Idaho Falls).
* [ ] Refactor the program to package it as a standalone executable (.exe) for easy distribution.