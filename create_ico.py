from PIL import Image, ImageDraw
import os

# Create a colorful icon
img = Image.new('RGBA', (256, 256), color=(255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a simple colorful design
draw.ellipse((50, 50, 206, 206), fill=(255, 100, 100, 255))
draw.ellipse((70, 70, 186, 186), fill=(100, 255, 100, 255))
draw.ellipse((90, 90, 166, 166), fill=(100, 100, 255, 255))

# Save as ICO directly
img.save('app_icon.ico', format='ICO')

print("Icon created as app_icon.ico") 