import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

# Default Parameters
path = r"Images"
image_width = 843
image_height = 1143
screen_width = 1920
screen_height = 1080

# Dictionary of images and their respective expressions
dict_img_exp = {'AF01HAS.jpg': 'Happiness', 'AM02HAS.jpg': 'Happiness', 'AF02HAS.jpg': 'Happiness', 
                'AM04HAS.jpg': 'Happiness', 'AF06HAS.jpg': 'Happiness', 'AM31HAS.jpg': 'Happiness', 
                'AF03SAS.jpg': 'Sadness', 'AM16SAS.jpg': 'Sadness', 'AF07SAS.jpg': 'Sadness', 
                'AM25SAS.jpg': 'Sadness', 'AF17SAS.jpg': 'Sadness', 'AM32SAS.jpg': 'Sadness', 
                'AF04NES.jpg': 'Neutrality', 'AM05NES.jpg': 'Neutrality', 'AF08NES.jpg': 'Neutrality', 
                'AM07NES.jpg': 'Neutrality', 'AF16NES.jpg': 'Neutrality', 'AM13NES.jpg': 'Neutrality', 
                'AF13AFS.jpg': 'Fear', 'AM08AFS.jpg': 'Fear', 'AF14AFS.jpg': 'Fear', 
                'AM14AFS.jpg': 'Fear', 'AF21AFS.jpg': 'Fear', 'AM23AFS.jpg': 'Fear', 
                'AF05ANS.jpg': 'Anger', 'AM10ANS.jpg': 'Anger', 'AF09ANS.jpg': 'Anger', 
                'AM17ANS.jpg': 'Anger', 'AF20ANS.jpg': 'Anger', 'AM29ANS.jpg': 'Anger' }

def show_image(imageFile, fixations = [], et_data = []):

    # Create background (this guarantees that the coordinate system will be preserved)
    background_color = (1, 0, 0)  # red
    background_width, background_height = screen_width, screen_height  
    background = np.ones((background_height, background_width, 3)) * background_color

    # Create a figure for background
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.imshow(background)
    ax.axis('off')
    #plt.show(block=False)

    # Load image
    image_path = os.path.join(path, imageFile)
    image = cv2.imread(image_path)
    # Adjust image size : resize to presentation values and crop
    resized_image = cv2.resize(image, (image_width, image_height))
    if image_width > screen_width:
        resized_image = resized_image[:, 0:screen_width, :] # not done by mean point
    if image_height > screen_height:
        diff = int((image_height-screen_height)/2)
        if (image_height-screen_height)%2:
            resized_image = resized_image[diff:image_height-diff-1, :, :]
        else:
            resized_image = resized_image[diff:image_height-diff, :, :]
    # Calculate origin on center of screen
    x_pos = int((screen_width - resized_image.shape[1]) / 2)
    y_pos = int((screen_height - resized_image.shape[0]) / 2)
    ax.imshow(resized_image, extent=[x_pos, x_pos + resized_image.shape[1], y_pos, y_pos + resized_image.shape[0]])

    if fixations != []:
        # Converting vertical coordinates (mirror effect)
        converted_fixations = [(x, screen_height - y) for x, y, *rest in fixations]
        # Draw fixation points
        for point in converted_fixations:
            ax.plot(point[0], point[1], 'bo', markersize=5)

    if et_data != []:
        # Converting vertical coordinates (mirror effect)
        converted_et_data = [(x, screen_height - y) for x, y, *rest in et_data]
        # Draw fixation points
        for point in converted_et_data:
            ax.plot(point[0], point[1], 'go', markersize=1)

    #ax.plot(-10,-10,'ro', markersize=5) # Debug

    plt.show(block=False)
    plt.pause(0.01)

