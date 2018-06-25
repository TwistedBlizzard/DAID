# DAID

DAID is a programmatic image downloader for DeviantArt written in Python by Josh Halsey.

## Getting Started

### Prerequisites

This project requires Python 3 with Selenium and a Google Chrome WebDriver.

Install Selenium through pip
```
pip install selenium
```
You will then need to follow this [guide](http://chromedriver.chromium.org/getting-started) to install the Google Chrome WebDriver.

### Running DAID

DAID is intended to be imported as a module rather than used as a standalone piece of software. There is however a simple demo that can be used to download image files.

To run this demo, simply run the script with Python. You will be presented with a command-line prompt for a search term.
Once you have entered the search term and pressed the return key, DAID will start gathering download links.
After DAID has finished gathering the download links, it will begin downloading images to <project_folder>/downloads/<search_term>.

Please be aware that the images downloaded with DAID remain the property of the artists and as such should not be used commercially without first obtaining permission.
