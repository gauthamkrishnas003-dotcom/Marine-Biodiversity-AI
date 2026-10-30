# Marine Biodiversity AI

A computer vision and data science project exploring deep-sea imagery
from the FathomNet dataset.

## Progress
- [x] Explored the FathomNet COCO annotation structure
- [x] Downloaded a sample of images using the FathomNet API
- [x] Visualised bounding boxes on images
- [ ] Analyse species distribution (common vs rare)
- [ ] Train a detection / classification model

## Dataset
FathomNet (https://fathomnet.org). Images and annotations are not
included in this repo. Credit: FathomNet and MBARI.

## Scripts
- `scripts/report.py` – inspect the JSON structure
- `scripts/top_animals.py` – most common animals
- `scripts/download_images.py` – download a sample of images
- `scripts/draw_boxes.py` – draw annotation boxes on images