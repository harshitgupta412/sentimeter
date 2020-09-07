# sentimeter

This is the project to scrape data related to a keyword from news websites, reddit and twitter and then do a sentiment analysis using NLTK or Flair.

The final_data.py is a scheduler script that fetches the data from the websites once per day. 

The data is stored in a google spreadsheet including the volume(number of data entries got) and the average sentiment for each of the sources and keys. 

The website folder contains the code for the site used to visualise the data using graphs.

### BEFORE USING THE SCRIPT
1. Replace the details for reddit api in the final_data.py
2. Make a Sentdex.json file containing the information about the google sheet you are using in the same directory as the final_data.py
3. Add the same data to Sentdex.json in website/sent
4. Install all the softwares listed in the requirements.txt
