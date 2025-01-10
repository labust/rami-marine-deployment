import cv2
import numpy as np
import matplotlib.pyplot as plt

#def color(photo,klasa)


image_path = 'D:/Lucija/PROJEKT_R/bove/crvene/img_0009.jpg'
image = cv2.imread(image_path)

# Convert BGR (OpenCV default) to RGB
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# Define RGB ranges for colors (with multiple ranges for the same color)
color_ranges = {
    "red": [  # Two ranges for red
        [(128, 0, 0), (255, 51, 51)],
        [(83, 82, 55), (133, 131, 102)],
        [( 138, 50, 74), (254, 154, 175)],
        [(122, 58, 70 ), (234, 159, 170)],
        [(165, 90, 97), ( 255, 195, 202)],
        [(148, 115, 85), (255, 222, 188)],
        [(113, 98, 68), (222, 203, 168)], 
        [(82, 105, 64), (186, 211, 164)], 
        [(177, 0, 10), (255, 115, 102)], 
        [(121, 0, 12), (242, 117, 102)], 
        [(99, 49, 44), (209, 147, 139)], 
        [(133, 98, 70), (245, 203, 171)],
        [(131, 100, 72), (242, 205, 174)],
        [(110, 72, 96), (217, 174, 200)], 
        [(76, 23, 19), (185, 118, 108)],
        [(156, 68, 42), (255, 172, 140)],
        [(131, 66, 40), (247, 168, 136)],
        [(177, 29, 97), (255, 148, 201)],
        [(180, 61, 97), (255, 170, 201)],
        [(182, 109, 114), (255, 217, 221)],
        [(86, 109, 68), (190, 216, 169)],
        [(62, 78, 48), (162, 180, 145)],
        [(128, 175, 104), (239, 255, 211)],
        [(156, 67, 41), (255, 171, 138)],
        [(173, 116, 82), (230, 180, 150)],
        [(139, 92, 60), (253, 196, 160)],
        [(133, 113, 69), (245, 220, 171)],
        [(119, 120, 75), (228, 227, 177)],
        [(162, 86, 58), (255, 191, 158)],
        [(136, 66, 41), (254, 168, 137)],
    ],
    "yellow": [  # One range for yellow
        [(194, 199, 0), (255, 255, 116)],
        [(125, 179, 60), (239, 255, 167)],
        [(196, 192, 88), (255, 255, 196)],
        [(178, 190, 84), (255, 255, 192)],
        [(151, 188, 97), (255, 255, 204)],
        [(139, 142, 39), (253, 252, 145)],
        [(128, 137, 25), (242, 246, 133)],
        [(115, 125, 41), (226, 233, 143)],
        [(189, 174, 0), (255, 255, 91)],
        [(165, 153, 0), (255, 255, 86)],
        [(109, 109, 0), (221, 215, 109)],
        [(196, 191, 28), (255, 255, 168)],
        [(197, 193, 95), (255, 255, 203)],
        [(142, 161, 47), (255, 255, 154)],
        [(114, 112, 6), (226, 218, 82)],
        [(100, 106, 31), (209, 211, 131)],
        [(113, 112, 22), (224, 219, 126)],
        [(119, 108, 0), (235, 213, 78)],
        [(196, 192, 76), (255, 255, 185)],
        [(145, 144, 0), (255, 253, 117)],
        [(157, 190, 92), (255, 255, 200)],
        [(52, 92, 0), (156, 197, 105)],
        [(192, 229, 152), (238, 255, 183)],
        [(194, 236, 140), (252, 255, 195)],
        [(148, 191, 138), (187, 248, 172)],
        [(118, 157, 81), (228, 255, 186)],
        [(66, 130, 66), (172, 239, 168)],

    ],
    "white": [  # One range for white
        [(200, 200, 200), (255, 255, 255)],
        [(195, 251, 244), (255, 255, 255)],
        [(190, 245, 233), (222, 255, 255)],
        [(226, 198, 194), (255, 235, 226)],
        [(178, 153, 129), (234, 217, 201)],
        [(244, 214, 222), (255, 255, 255)],
        [(232, 182, 185), (255, 238, 241)],
        [(180, 158, 153), (236, 213, 207)],
        [(140, 242, 212), (198, 255, 255)],
        [(120, 236, 190), (157, 255, 237)],
        [(163, 167, 132), (218, 222, 185)],
        [(55, 227, 225), (145, 255, 255)],
        [(55, 191, 191), (122, 248, 247)],
        [(71, 162, 112), (141, 217, 173)],
        [(143, 239, 206), (178, 255, 255)],
        [(120, 237, 197), (158, 255, 245)],
        [(115, 236, 195), (153, 255, 243)]
    ]
}

# Create combined masks for each color
masks = {}
for color, ranges in color_ranges.items():
    mask_combined = None
    for lower, upper in ranges:
        lower_bound = np.array(lower, dtype=np.uint8)
        upper_bound = np.array(upper, dtype=np.uint8)
        mask = cv2.inRange(image_rgb, lower_bound, upper_bound)
        
        # Combine masks for multiple ranges (bitwise OR)
        if mask_combined is None:
            mask_combined = mask
        else:
            mask_combined = cv2.bitwise_or(mask_combined, mask)
    
    masks[color] = mask_combined

# Apply the masks to extract the regions for each color
color_regions = {}
for color, mask in masks.items():
    color_regions[color] = cv2.bitwise_and(image_rgb, image_rgb, mask=mask)

# Count the number of pixels for each color mask
color_pixel_count = {color: cv2.countNonZero(mask) for color, mask in masks.items()}

# Determine the dominant color
dominant_color = max(color_pixel_count, key=color_pixel_count.get)

# Print the dominant color
print(f"Dominant color: {dominant_color}")

# Display the original image and the regions for each color using matplotlib
plt.figure(figsize=(12, 8))

'''# Plot the original image
plt.subplot(2, 2, 1)
plt.imshow(image_rgb)
plt.title("Original Image")
plt.axis("off")

# Plot each color region
for i, (color, region) in enumerate(color_regions.items(), start=2):
    plt.subplot(2, 2, i)
    plt.imshow(region)
    plt.title(f"{color.capitalize()} Region")
    plt.axis("off")

plt.tight_layout()
plt.show()'''

#return dominant_color
