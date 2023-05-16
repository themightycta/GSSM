import os
import tkinter as tk
from tkinter import filedialog
from PIL import Image

# Initialize Tkinter
root = tk.Tk()
root.title("SpriteSheet Generator")
root.geometry("400x300")

# List to store selected image paths
image_paths = []


def select_images():
    # Open file dialog to select multiple images
    files = filedialog.askopenfilenames(title="Select Images",
                                        filetypes=(("Image Files", "*.png;*.jpg;*.jpeg"), ("All Files", "*.*")))

    # Add selected images to the list
    for file in files:
        image_paths.append(file)

    # Update image count label
    image_count_label.config(text="Selected Images: " + str(len(image_paths)))


def generate_spritesheet():
    if len(image_paths) == 0:
        return

    # Create a new blank image for spritesheet
    spritesheet = Image.new('RGBA', (100 * len(image_paths), 100))

    # Create an XML string for animation data
    xml_data = '<spritesheet>\n\t<parts>\n'

    # Iterate through the selected images and paste them onto the spritesheet
    for i, image_path in enumerate(image_paths):
        image = Image.open(image_path)
        image = image.resize((100, 100), Image.ANTIALIAS)

        spritesheet.paste(image, (i * 100, 0))

        xml_data += f'\t\t<part name="{os.path.basename(image_path)}" x="{i * 100}" y="0" width="100" height="100" />\n'

    xml_data += '\t</parts>\n</spritesheet>'

    # Save the spritesheet as PNG
    spritesheet_path = filedialog.asksaveasfilename(title="Save Spritesheet",
                                                    filetypes=(("PNG Files", "*.png"), ("All Files", "*.*")),
                                                    defaultextension=".png")
    spritesheet.save(spritesheet_path)

    # Save the XML file
    xml_path = spritesheet_path[:-4] + ".xml"
    with open(xml_path, 'w') as xml_file:
        xml_file.write(xml_data)

    # Reset the image paths list
    image_paths.clear()
    image_count_label.config(text="Selected Images: 0")


# Button to select images
select_button = tk.Button(root, text="Select Images", command=select_images)
select_button.pack(pady=10)

# Label to display selected image count
image_count_label = tk.Label(root, text="Selected Images: 0")
image_count_label.pack()

# Button to generate spritesheet
generate_button = tk.Button(root, text="Generate Spritesheet", command=generate_spritesheet)
generate_button.pack(pady=10)

# Start the Tkinter event loop
root.mainloop()
