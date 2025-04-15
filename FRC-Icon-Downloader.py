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

def download_avatars():
    """
    Downloads FRC team avatars for the Ontario district from The Blue Alliance.
    """
    print(f"Fetching team list from: {EVENT_PAGE_URL}")

    try:
        # Fetch the HTML content of the event page
        response = requests.get(EVENT_PAGE_URL, timeout=30) # Added timeout
        response.raise_for_status() # Raise an exception for bad status codes (4xx or 5xx)
    except requests.exceptions.RequestException as e:
        print(f"Error fetching event page: {e}")
        return

    # Parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find team numbers - they are usually in links like '/team/1114/2025' within the teams table
    team_numbers = set() # Use a set to avoid duplicates
    # Look for links within the specific teams table if possible, otherwise search all links
    teams_table = soup.find('table', {'id': 'eventTeamsTable'}) # Adjust if ID changes
    links_to_check = teams_table.find_all('a') if teams_table else soup.find_all('a')

    for link in links_to_check:
        href = link.get('href', '')
        # Regex to match '/team/[number]' or '/team/[number]/[year]'
        match = re.match(r'/team/(\d+)(?:/\d+)?$', href)
        if match:
            team_number = match.group(1)
            team_numbers.add(team_number)

    if not team_numbers:
        print("Could not find any team numbers on the page. The website structure might have changed.")
        return

    print(f"Found {len(team_numbers)} teams.")

    # Create the output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        print(f"Creating output folder: {OUTPUT_FOLDER}")
        os.makedirs(OUTPUT_FOLDER)
    else:
        print(f"Output folder already exists: {OUTPUT_FOLDER}")

    # Download avatars
    downloaded_count = 0
    skipped_count = 0
    error_count = 0

    sorted_teams = sorted(list(team_numbers), key=int) # Sort numerically

    print("\nStarting avatar download...")
    for team_number in sorted_teams:
        # Construct the avatar URL
        avatar_path = f"/avatar/{AVATAR_YEAR}/frc{team_number}.png"
        avatar_url = BASE_AVATAR_URL + avatar_path
        output_filename = f"frc{team_number}.png"
        output_filepath = os.path.join(OUTPUT_FOLDER, output_filename)

        print(f"Attempting to download avatar for team {team_number} from {avatar_url}...")

        try:
            # Add a small delay
            time.sleep(REQUEST_DELAY_SECONDS)

            # Get the image data
            avatar_response = requests.get(avatar_url, stream=True, timeout=15) # stream=True for images, added timeout

            # Check if the download was successful (status code 200)
            if avatar_response.status_code == 200:
                # Check content type to ensure it's an image (optional but good practice)
                content_type = avatar_response.headers.get('content-type', '')
                if 'image' in content_type:
                    # Save the image to the output folder
                    with open(output_filepath, 'wb') as f:
                        for chunk in avatar_response.iter_content(1024): # Write in chunks
                            f.write(chunk)
                    print(f"  Successfully downloaded and saved: {output_filename}")
                    downloaded_count += 1
                else:
                    print(f"  Skipped: URL did not return an image (Content-Type: {content_type})")
                    skipped_count += 1
            elif avatar_response.status_code == 404:
                print(f"  Skipped: Avatar not found for team {team_number} (404 Error)")
                skipped_count += 1
            else:
                print(f"  Error: Received status code {avatar_response.status_code} for team {team_number}")
                error_count += 1
                # Optionally log the specific error: print(avatar_response.text)

        except requests.exceptions.RequestException as e:
            print(f"  Error downloading avatar for team {team_number}: {e}")
            error_count += 1
        except IOError as e:
            print(f"  Error saving file {output_filename}: {e}")
            error_count += 1

    print("\n--- Download Summary ---")
    print(f"Total teams found: {len(team_numbers)}")
    print(f"Successfully downloaded: {downloaded_count}")
    print(f"Skipped (e.g., not found): {skipped_count}")
    print(f"Errors: {error_count}")
    print(f"Avatars saved in folder: '{OUTPUT_FOLDER}'")

# --- Run the script ---
if __name__ == "__main__":
    download_avatars()
