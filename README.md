# FRC-Team-Icon-Downloader

----------Features----------

This program will create a new folder in the programs directory
It will then download the team icon of every FRC team within the specified district from The Blue Alliance website
If a team does not have a logo it will be skipped or marked as an error
A summary of the downloads will be sent at the end listing the following:

Total teams found, Sucessful downloads, Skipped downloads, Errors, and save folder name

There is a sample output folder in this repository so you can see what the final output will look like

----------Instructions----------

pip install requests and bs4
In the configuration section: paste the blue alliance link containing the list of teams you want to download
Change the avatar year as needed
Adjust output folder name to your preference
Request delay is set to 0.5 seconds by default to not cause any issues on the server but this can be updated as needed
