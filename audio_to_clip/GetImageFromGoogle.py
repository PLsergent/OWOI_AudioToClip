import requests
import urllib.request
import random
from PIL import Image
from audio_to_clip.WordTimestamp import WordTimestamp


# Replace YOUR_API_KEY with your actual API key
API_KEY = 'AIzaSyD-PdqIeea1pV5JQNX6lFDndXMV9theIvM'

# Replace YOUR_CX with your actual Custom Search Engine ID
CSE_ID = '001937365010730226554:ccxz10b7hba'

# Set the search query
query = 'flowers'

# Set the number of results you want to retrieve
num = 5

# Set the image size to large
imgSize = 'large'

# Set the image type to photo
imgType = 'photo'

# Set the search type to image
searchType = 'image'

# Set the URL for the search request
url = "https://www.googleapis.com/customsearch/v1?key=" + API_KEY + "&cx=" + CSE_ID + "&q=" + query + "&searchType=" + searchType + "&imgSize=" + imgSize + "&imgType=" + imgType + "&num=" + str(num)

# Send the request and retrieve the results
response = requests.get(url)

# Get the list of image URLs from the response
image_urls = response.json()['items']

# Select a random image URL from the list
random_image_url = random.choice(image_urls)['link']


#PATH to save the image
PATH = 'C:\\Users\\zorro\\OneDrive\\Documents\\EFREI\\M2\\Projet Transverse\\image\\'

#Name of the image and extension
ImageName = query+'.jpg'

# Select a random image URL from the list
random_image_url = random.choice(image_urls)['link']

#Path of the file
ImagePATH = PATH+ImageName
urllib.request.urlretrieve(random_image_url, ImagePATH)
# Open the image file using Pillow
image = Image.open(ImagePATH)

# Resize the image to 500x500 pixels
image = image.resize((500, 500))

# Save the resized image to a new file
image.save(ImagePATH)