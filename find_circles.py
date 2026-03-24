import sys
try:
    from PIL import Image
    import numpy as np
except ImportError:
    print("Please install Pillow and numpy")
    sys.exit(1)

img = Image.open('dmg_background.png').convert('RGB')
arr = np.array(img)
h, w, c = arr.shape
print(f"Dimensions: {w}x{h}")

# In typical DMG backgrounds, there are markers or circles for the icons.
# We'll just look for non-background colors or prominent shapes to guess perfectly centered icon positions.
# Let's find the prominent horizontal regions.
