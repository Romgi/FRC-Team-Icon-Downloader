import requests
import os
import re
from bs4 import BeautifulSoup
import time

# --- Configuration ---
EVENT_PAGE_URL = "https://www.thebluealliance.com/events/ont#teams"
BASE_AVATAR_URL = "https://www.thebluealliance.com"
# Use the year specified in the avatar path example
# You might need to change this year depending on the current season
AVATAR_YEAR = 2025
OUTPUT_FOLDER = "team icons"
# Add a small delay between requests to be polite to the server
REQUEST_DELAY_SECONDS = 0.5
# --- End Configuration ---