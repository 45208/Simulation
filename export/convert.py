import glob
from pathlib import Path
import imageio
FOLDER_NAME = "images\\boardx_soly"

def srt(a: str):
    return int(Path(a).stem)

image_names = glob.glob(f"{FOLDER_NAME}\\*.png")
image_names = sorted(image_names, key=srt)

images = []
for name in image_names:
    images.append(imageio.imread(name))

imageio.mimsave(f"{FOLDER_NAME}\\result.gif", images)
