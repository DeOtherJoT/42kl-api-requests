from PIL import Image
import os

# Set the size for each image in the collage (3cm x 3cm)
image_size = (300, 300)  # 1 cm = 100 pixels

# Create a list to store all the image paths
image_paths = []

# Replace 'path_to_your_folder' with the path to your folder containing images
folder_path = './generate-collage/cadets-pictures'

# Loop through all files in the folder
for filename in os.listdir(folder_path):
    if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
        image_paths.append(os.path.join(folder_path, filename))

# Calculate the number of rows and columns based on the number of images
num_images = len(image_paths)
num_columns = 23
num_rows = 90

# Calculate the size of the collage image
collage_size = (num_columns * image_size[0], num_rows * image_size[1])

collage_width = 70 * 100  # 1 cm = 100 pixels
collage_height = 140 * 100

# Create a new blank image for the collage
collage = Image.new('RGB', (collage_width, collage_height), (255, 255, 255))

# Paste each image into the collage
for i, image_path in enumerate(image_paths):
    x = (i % num_columns) * image_size[0]
    y = (i // num_columns) * image_size[1]
    img = Image.open(image_path)
    img = img.resize(image_size)
    collage.paste(img, (x, y))

# Save the collage
collage.save('output_collage.jpg')

# Optional: Display the collage
collage.show()