import requests
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import json

# Download the necessary NLTK data
#nltk.download('punkt')

# List of URLs to scrape
urls = ['/wiki/China', '/wiki/India', '/wiki/United_States', '/wiki/Indonesia', '/wiki/Pakistan', '/wiki/Nigeria', '/wiki/Brazil', '/wiki/Bangladesh', '/wiki/Russia', '/wiki/Mexico', '/wiki/Japan', '/wiki/Philippines', '/wiki/Ethiopia', '/wiki/Egypt', '/wiki/Vietnam', '/wiki/Democratic_Republic_of_the_Congo', '/wiki/Iran', '/wiki/Turkey', '/wiki/Germany', '/wiki/Thailand', '/wiki/France', '/wiki/United_Kingdom', '/wiki/South_Africa', '/wiki/Tanzania', '/wiki/Italy', '/wiki/Myanmar', '/wiki/Colombia', '/wiki/Kenya', '/wiki/South_Korea', '/wiki/Spain', '/wiki/Argentina', '/wiki/Algeria', '/wiki/Iraq', '/wiki/Uganda', '/wiki/Sudan', '/wiki/Ukraine', '/wiki/Canada', '/wiki/Poland', '/wiki/Morocco', '/wiki/Uzbekistan', '/wiki/Afghanistan', '/wiki/Peru', '/wiki/Malaysia', '/wiki/Angola', '/wiki/Mozambique', '/wiki/Saudi_Arabia', '/wiki/Yemen', '/wiki/Ghana', '/wiki/Ivory_Coast', '/wiki/Nepal', '/wiki/Venezuela', '/wiki/Cameroon', '/wiki/Madagascar', '/wiki/Australia', '/wiki/North_Korea', '/wiki/Niger', '/wiki/Taiwan', '/wiki/Syria', '/wiki/Mali', '/wiki/Burkina_Faso', '/wiki/Sri_Lanka', '/wiki/Malawi', '/wiki/Chile', '/wiki/Kazakhstan', '/wiki/Zambia', '/wiki/Romania', '/wiki/Senegal','/wiki/Somalia', '/wiki/Netherlands', '/wiki/Guatemala', '/wiki/Chad', '/wiki/Cambodia', '/wiki/Ecuador', '/wiki/Zimbabwe', '/wiki/Guinea', '/wiki/South_Sudan', '/wiki/Rwanda', '/wiki/Burundi', '/wiki/Benin', '/wiki/Bolivia', '/wiki/Tunisia', '/wiki/Papua_New_Guinea', '/wiki/Belgium']

# Initialize the stemmer
stemmer = PorterStemmer()

# List to store JSON data for each page
all_data = {
    "countries": []
}

# Iterate through each URL
for url in urls:
    print("Processing:", url)

    # Send an HTTP GET request to the URL
    response = requests.get("https://en.wikipedia.org" + url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the title of the page
        title = soup.find("h1", {"id": "firstHeading"})
        page_title = title.text

        # Find the specific div with the ID "mw-content-text"
        content = soup.find("div", {"id": "mw-content-text"})

        # Find and extract the subtitles
        subtitles = content.find_all(["h1", "h2", "h3", "h4", "h5", "h6"])

        # Find and extract the images
        images = content.find_all("img")

        # Find all <cite> tags within the references section
        cites = content.find_all("cite")

        # Create a dictionary to store the data
        country_data = {
            "title": {
                "original": page_title,
                "stemmed": stemmer.stem(page_title)
            },
            "subtitles": [],
            "images": [],
            "references": []
        }

        current_header = None

        for subtitle in subtitles:
            subtitle_text = subtitle.text
            subtitle_name = subtitle.name

            # Skip if the subtitle is "References"
            if subtitle_text.lower() == "references":
                continue
            
            # Find all paragraphs below each subtitle
            paragraphs = []
            next_sibling = subtitle.find_next_sibling()
            while next_sibling:
                try:
                    # Break if the next sibling is a header
                    if next_sibling.name and next_sibling.name.startswith('h'):
                        break
                    
                    # Append paragraphs if the next sibling is a paragraph
                    if next_sibling.name == 'p':
                        paragraphs.append(next_sibling)

                    # Move to the next sibling
                    next_sibling = next_sibling.find_next_sibling()

                except AttributeError:
                    # Handle AttributeError (e.g., when next_sibling is None)
                    break
                
            # Apply stemming to each word in the text and add tags
            stemmed_paragraphs = []
            for paragraph in paragraphs:
                words = word_tokenize(paragraph.text)

                # Apply stemming to each word
                stemmed_words = [stemmer.stem(word) for word in words]

                # Add tags based on the HTML tags
                tagged_words = [{"word": word, "tag": paragraph.name} for word in stemmed_words]

                # Store the stemmed words with tags
                stemmed_paragraphs.append(tagged_words)

            # Apply stemming to each word in the subtitle text
            words_in_subtitle = word_tokenize(subtitle_text)
            stemmed_subtitle_words = [stemmer.stem(word) for word in words_in_subtitle]

            # Add tags based on the HTML tag
            tagged_subtitle_words = [{"word": word, "tag": subtitle.name} for word in stemmed_subtitle_words]

            # Store both original and stemmed text under each subtitle
            country_data["subtitles"].append({
                "subtitle": subtitle_text,
                "tag": subtitle_name,
                "original": {
                    "full_text": " ".join([paragraph.text for paragraph in paragraphs]),
                    "paragraphs": [paragraph.text for paragraph in paragraphs]
                },
                "stemmed": {
                    "stemmed_subtitle": stemmed_subtitle_words,
                    "stemmed_words": stemmed_paragraphs
                }
            })

        # Iterate over images and extract src and alt
        for image in images:
            image_src = image.get("src", "")
            image_alt = image.get("alt", "")

            # Apply stemming to each word in the alt text
            words_in_alt = word_tokenize(image_alt)
            stemmed_alt_words = [stemmer.stem(word) for word in words_in_alt]

            # Store image information with stemming for alt text
            country_data["images"].append({
                "src": image_src,
                "alt": {
                    "original": image_alt,
                    "stemmed_words": stemmed_alt_words
                }
            })

        # Iterate over <cite> tags within the references section and extract information
        for index, cite in enumerate(cites, start=1):
            # Extract information from the <cite> tag
            authors_tag = cite.find("a")
            description_tag = cite.find("i")

            # Check if both authors and description tags are available
            if authors_tag:
                authors = authors_tag.text
                words_in_author = word_tokenize(authors)
                authors_stemmed = [stemmer.stem(word) for word in words_in_author] # Apply stemming
                link = authors_tag.get("href", "") # Apply stemming
                words_in_link = word_tokenize(link)
                link_stemmed = [stemmer.stem(word) for word in words_in_link]
            else:
                authors = "",
                authors_stemmed = ""
                link = ""
                link_stemmed = ""
            
            if description_tag:
                description = description_tag.text
                words_in_description = word_tokenize(description)
                description_stemmed = [stemmer.stem(word) for word in words_in_description] # Apply stemming 
            else:
                description = ""
                description_stemmed = ""
                
            # Store reference information with stemming and the citation number
            country_data["references"].append({
                "cite_number": index,
                "authors": {
                    "original": authors,
                    "stemmed": authors_stemmed
                },
                "link": {
                    "original": link,
                    "stemmed": link_stemmed
                },
                "description": {
                    "original": description,
                    "stemmed": description_stemmed
                },
                "tags": [{"word": word, "tag": description_tag.name} for word in word_tokenize(description)]
            })

        print(f"Data for {url} has been processed.")
        # Append the data for this page to the list
        all_data["countries"].append(country_data)

    else:
        print(f"Failed to retrieve the article from {url}")

# Serialize the data for all pages to a JSON-formatted string
big_json_data = json.dumps(all_data, indent=4)
#big_json_data = json.dumps(all_data, separators=(',', ':'))

print("writing on .txt")
# Save the big JSON-formatted data to a .txt file
with open(r"C:\Users\Brend\OneDrive\Escritorio\wikipedia_data_pequeno.txt", "w") as txt_file:
    txt_file.write(big_json_data)

print("wikipedia_data.txt")