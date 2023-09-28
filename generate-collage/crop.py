import cv2
import numpy as np

# Load the face detection model (Haar Cascades)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Function to crop and center the face with a larger portion
def crop_and_center_face(image_path, output_path, scale_factor=1.5, target_size=(300, 300)):
    # Load the image
    image = cv2.imread(image_path)
    
    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # If faces are found
    if len(faces) > 0:
        x, y, w, h = faces[0]  # Assuming the first detected face is the main subject
        
        # Calculate the ROI around the detected face with a scale factor
        roi_x = max(0, x - int((scale_factor - 1) * w / 2))
        roi_y = max(0, y - int((scale_factor - 1) * h / 2))
        roi_w = min(image.shape[1] - roi_x, int(scale_factor * w))
        roi_h = min(image.shape[0] - roi_y, int(scale_factor * h))
        
        face = image[roi_y:roi_y+roi_h, roi_x:roi_x+roi_w]  # Crop the face
        
        # Resize the cropped face to the target size
        face = cv2.resize(face, target_size)
        
        # Save the centered face
        cv2.imwrite(output_path, face)
        
        print(f"Face cropped and centered: {output_path}")
    else:
        print(f"No faces found in: {image_path}")

# Process your images
output_folder = "output_faces/"

# Create the output folder if it doesn't exist
import os
os.makedirs(output_folder, exist_ok=True)

# Specify the directory path
directory_path = './cadets-pictures'

# Initialize an empty list to store file names
input_image_paths = []
# Iterate through the directory
for filename in os.listdir(directory_path):
    # Check if the path is a file (not a directory)
    if os.path.isfile(os.path.join(directory_path, filename)):
        input_image_paths.append("./cadets-pictures/" + filename)
print(input_image_paths)
for input_image_path in input_image_paths:
    output_image_path = os.path.join(output_folder, os.path.basename(input_image_path))
    crop_and_center_face(input_image_path, output_image_path)

print("Processing complete.")