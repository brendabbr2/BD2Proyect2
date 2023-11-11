import requests
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
import json
import nltk

# Download the necessary NLTK data
nltk.download('punkt')

# List of URLs to scrape
urls = ['/wiki/China', '/wiki/India', '/wiki/United_States', '/wiki/Indonesia', '/wiki/Pakistan', '/wiki/Nigeria', '/wiki/Brazil', '/wiki/Bangladesh', '/wiki/Russia', '/wiki/Mexico', '/wiki/Japan', '/wiki/Philippines', '/wiki/Ethiopia', '/wiki/Egypt', '/wiki/Vietnam', '/wiki/Democratic_Republic_of_the_Congo', '/wiki/Iran', '/wiki/Turkey', '/wiki/Germany', '/wiki/Thailand', '/wiki/France', '/wiki/United_Kingdom', '/wiki/South_Africa', '/wiki/Tanzania', '/wiki/Italy', '/wiki/Myanmar', '/wiki/Colombia', '/wiki/Kenya', '/wiki/South_Korea', '/wiki/Spain', '/wiki/Argentina', '/wiki/Algeria', '/wiki/Iraq', '/wiki/Uganda', '/wiki/Sudan', '/wiki/Ukraine', '/wiki/Canada', '/wiki/Poland', '/wiki/Morocco', '/wiki/Uzbekistan', '/wiki/Afghanistan', '/wiki/Peru', '/wiki/Malaysia', '/wiki/Angola', '/wiki/Mozambique', '/wiki/Saudi_Arabia', '/wiki/Yemen', '/wiki/Ghana', '/wiki/Ivory_Coast', '/wiki/Nepal', '/wiki/Venezuela', '/wiki/Cameroon', '/wiki/Madagascar', '/wiki/Australia', '/wiki/North_Korea', '/wiki/Niger', '/wiki/Taiwan', '/wiki/Syria', '/wiki/Mali', '/wiki/Burkina_Faso', '/wiki/Sri_Lanka', '/wiki/Malawi', '/wiki/Chile', '/wiki/Kazakhstan', '/wiki/Zambia', '/wiki/Romania', '/wiki/Senegal', '/wiki/Somalia', '/wiki/Netherlands', '/wiki/Guatemala', '/wiki/Chad', '/wiki/Cambodia', '/wiki/Ecuador', '/wiki/Zimbabwe', '/wiki/Guinea', '/wiki/South_Sudan', '/wiki/Rwanda', '/wiki/Burundi', '/wiki/Benin', '/wiki/Bolivia', '/wiki/Tunisia', '/wiki/Papua_New_Guinea', '/wiki/Belgium', '/wiki/Haiti', '/wiki/Jordan', '/wiki/Cuba', '/wiki/Czech_Republic', '/wiki/Dominican_Republic', '/wiki/Sweden', '/wiki/Greece', '/wiki/Portugal', '/wiki/Azerbaijan', '/wiki/Tajikistan', '/wiki/Israel', '/wiki/Honduras', '/wiki/Hungary', '/wiki/United_Arab_Emirates', '/wiki/Belarus', '/wiki/Austria', '/wiki/Switzerland', '/wiki/Sierra_Leone', '/wiki/Togo', '/wiki/Hong_Kong', '/wiki/Laos', '/wiki/Kyrgyzstan', '/wiki/Turkmenistan', '/wiki/Libya', '/wiki/El_Salvador', '/wiki/Nicaragua', '/wiki/Serbia', '/wiki/Bulgaria', '/wiki/Paraguay', '/wiki/Republic_of_the_Congo', '/wiki/Denmark', '/wiki/Singapore', '/wiki/Central_African_Republic', '/wiki/Finland', '/wiki/Norway', '/wiki/Lebanon', '/wiki/State_of_Palestine', '/wiki/Slovakia', '/wiki/Republic_of_Ireland', '/wiki/Costa_Rica', '/wiki/Liberia', '/wiki/New_Zealand', '/wiki/Oman', '/wiki/Kuwait', '/wiki/Mauritania', '/wiki/Panama', '/wiki/Croatia', '/wiki/Eritrea', '/wiki/Georgia_(country)', '/wiki/Uruguay', '/wiki/Mongolia', '/wiki/Bosnia_and_Herzegovina', '/wiki/Puerto_Rico', '/wiki/Armenia', '/wiki/Lithuania', '/wiki/Jamaica', '/wiki/Albania', '/wiki/Qatar', '/wiki/Namibia', '/wiki/Moldova', '/wiki/The_Gambia', '/wiki/Botswana', '/wiki/Lesotho', '/wiki/Gabon', '/wiki/Slovenia', '/wiki/Latvia', '/wiki/North_Macedonia', '/wiki/Guinea-Bissau', '/wiki/Kosovo', '/wiki/Bahrain', '/wiki/Equatorial_Guinea', '/wiki/Estonia', '/wiki/Trinidad_and_Tobago', '/wiki/East_Timor', '/wiki/Mauritius', '/wiki/Eswatini', '/wiki/Djibouti', '/wiki/Cyprus', '/wiki/Fiji', '/wiki/Bhutan', '/wiki/Comoros', '/wiki/Guyana', '/wiki/Solomon_Islands', '/wiki/Macau', '/wiki/Luxembourg', '/wiki/Montenegro', '/wiki/Suriname', '/wiki/Western_Sahara', '/wiki/Malta', '/wiki/Cape_Verde', '/wiki/Brunei', '/wiki/Belize', '/wiki/The_Bahamas', '/wiki/Iceland', '/wiki/Northern_Cyprus', '/wiki/Maldives', '/wiki/Transnistria', '/wiki/Vanuatu', '/wiki/French_Polynesia', '/wiki/New_Caledonia', '/wiki/Barbados', '/wiki/Abkhazia', '/wiki/S%C3%A3o_Tom%C3%A9_and_Pr%C3%ADncipe', '/wiki/Samoa', '/wiki/Saint_Lucia', '/wiki/Guam', '/wiki/Cura%C3%A7ao', '/wiki/Republic_of_Artsakh', '/wiki/Kiribati', '/wiki/Grenada', '/wiki/Saint_Vincent_and_the_Grenadines', '/wiki/Aruba', '/wiki/Federated_States_of_Micronesia', '/wiki/Jersey', '/wiki/Antigua_and_Barbuda', '/wiki/Seychelles', '/wiki/Tonga', '/wiki/United_States_Virgin_Islands', '/wiki/Isle_of_Man', '/wiki/Andorra', '/wiki/Cayman_Islands', '/wiki/Dominica', '/wiki/Guernsey', '/wiki/Bermuda', '/wiki/Greenland', '/wiki/South_Ossetia', '/wiki/Faroe_Islands', '/wiki/American_Samoa', '/wiki/Northern_Mariana_Islands', '/wiki/Saint_Kitts_and_Nevis', '/wiki/Turks_and_Caicos_Islands', '/wiki/Sint_Maarten', '/wiki/Marshall_Islands', '/wiki/Liechtenstein', '/wiki/Monaco', '/wiki/Gibraltar', '/wiki/San_Marino', '/wiki/Collectivity_of_Saint_Martin', '/wiki/British_Virgin_Islands', '/wiki/%C3%85land', '/wiki/Palau', '/wiki/Anguilla', '/wiki/Cook_Islands', '/wiki/Nauru', '/wiki/Wallis_and_Futuna', '/wiki/Tuvalu', '/wiki/Saint_Barth%C3%A9lemy', '/wiki/Saint_Pierre_and_Miquelon', '/wiki/Saint_Helena,_Ascension_and_Tristan_da_Cunha', '/wiki/Montserrat', '/wiki/Falkland_Islands', '/wiki/Norfolk_Island', '/wiki/Christmas_Island', '/wiki/Tokelau', '/wiki/Niue', '/wiki/Vatican_City', '/wiki/Cocos_(Keeling)_Islands', '/wiki/Pitcairn_Islands']

# Initialize the stemmer
stemmer = PorterStemmer()

# List to store JSON data for each page
all_data = []

# Iterate through each URL
for url in urls:
    # Send an HTTP GET request to the URL
    response = requests.get("https://en.wikipedia.org" + url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the title of the page
        title = soup.find("h1", {"id": "firstHeading"})
        page_title = title.text

        # Find and extract the subtitles
        subtitles = soup.find_all(["h2", "h3"])

        # Find and extract the images
        images = soup.find_all("img")

        # Find all <cite> tags within the references section
        cites = soup.find_all("cite")

        # Create a dictionary to store the data for this page
        data = {
            "title": {
                "original": page_title,
                "stemmed": stemmer.stem(page_title)
            },
            "subtitles": {},
            "images": [],
            "references": []
        }

        # Iterate over subtitles and extract text
        for subtitle in subtitles:
            subtitle_text = subtitle.text

            # Skip if the subtitle is "References"
            if subtitle_text.lower() == "references":
                continue

            # Find all paragraphs below each subtitle
            paragraphs = subtitle.find_all_next(["p"])

            # Apply stemming to the text
            full_text_stemmed = stemmer.stem(" ".join([paragraph.text for paragraph in paragraphs]))
            paragraphs_stemmed = [stemmer.stem(paragraph.text) for paragraph in paragraphs]

            # Store both original and stemmed text under each subtitle
            data["subtitles"][subtitle_text] = {
                "original": {
                    "full_text": " ".join([paragraph.text for paragraph in paragraphs]),
                    "paragraphs": [paragraph.text for paragraph in paragraphs]
                },
                "stemmed": {
                    "full_text": full_text_stemmed,
                    "paragraphs": paragraphs_stemmed
                }
            }

        # Iterate over images and extract src and alt
        for image in images:
            image_src = image.get("src", "")
            image_alt = image.get("alt", "")

            # Apply stemming to the alt text
            image_alt_stemmed = stemmer.stem(image_alt)

            # Store image information with stemming
            data["images"].append({
                "src": image_src,
                "alt": {
                    "original": image_alt,
                    "stemmed": image_alt_stemmed
                }
            })

        # Iterate over <cite> tags within the references section and extract information
        for index, cite in enumerate(cites, start=1):
            # Extract information from the <cite> tag
            authors_tag = cite.find("a")
            description_tag = cite.find("i")

            # Check if both authors and description tags are available
            if authors_tag and description_tag:
                authors = authors_tag.text
                link = authors_tag.get("href", "")
                description = description_tag.text

                # Apply stemming to the authors and description
                authors_stemmed = stemmer.stem(authors)
                description_stemmed = stemmer.stem(description)

                # Store reference information with stemming
                data["references"].append({
                    "citation_number": index,
                    "authors": {
                        "original": authors,
                        "stemmed": authors_stemmed
                    },
                    "link": {
                        "original": link,
                        "stemmed": stemmer.stem(link)
                    },
                    "description": {
                        "original": description,
                        "stemmed": description_stemmed
                    }
                })

        # Append the data for this page to the list
        all_data.append(data)

    else:
        print(f"Failed to retrieve the article from {url}")

# Serialize the data for all pages to a JSON-formatted string
big_json_data = json.dumps(all_data, indent=4)

# Save the big JSON-formatted data to a .txt file
with open(r"C:\Users\Brend\OneDrive\Escritorio\wikipedia_data.txt", "w") as txt_file:
    txt_file.write(big_json_data)

print("wikipedia_data.txt")
