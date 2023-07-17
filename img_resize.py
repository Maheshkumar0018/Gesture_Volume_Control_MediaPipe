import cv2
import os

def resize_and_save_images(input_folder, output_folder, target_size):
    for filename in os.listdir(input_folder):
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, filename)
        image = cv2.imread(input_path)
        resized_image = cv2.resize(image, target_size)
        cv2.imwrite(output_path, resized_image)

input_folder = './FingerImages'
output_folder = './fingersimg'
target_size = (200, 200) 

resize_and_save_images(input_folder, output_folder, target_size)

