import os
from PIL import Image
import pymeshlab


path = os.getcwd()

image_name = input("Insert 2D image file name \n")
image_type = input("Insert 2D image file type \n")
input_image = path + "\\appwin\\2d_images\\" + image_name + "." + image_type

#Prepare Superpixels
sigma = " 0.8 "
k = " 100 "
min = " 100 "
segment_path = path + '\\appwin\\segment.exe'
input_superpixel = path + "\\appwin\\in_superpixels\\" + image_name + ".ppm"
im = Image.open(input_image)
im.save(input_superpixel)
output_superpixel = path + "\\appwin\\2d_images\\" + image_name + ".ppm"
segment_command = segment_path + sigma + k + min + input_superpixel + " " + output_superpixel

#Execute Superpixels
print("Creating Superpixels...")
stream = os.popen(segment_command)
output = stream.read()
print("Superpixels Created")

popup_path = path + '\\appwin\\photoPopup.exe'
classifier_path = "./classifiers_08_22_2005 "
popup_input = "./2d_images/" + image_name + "." + image_type
superpixel_extension = " ppm "
result_dir = path + "\\appwin\\popup_results\\" + image_name

if not(os.path.isdir(result_dir)):
    os.mkdir(result_dir)

popup_results = "./popup_results/" + image_name

popup_command = popup_path + " " + classifier_path + popup_input + superpixel_extension + popup_results


#Execute Automatic Photo Popup
print("Creating Photo-Popup...")
os.chdir(path + "\\appwin")
stream = os.popen(popup_command)
output = stream.read()
print("Photo-popup Created")

# ms = pymeshlab.MeshSet()
# ms.load_new_mesh('alley.x3d')
# ms.save_current_mesh('alley.obj')


