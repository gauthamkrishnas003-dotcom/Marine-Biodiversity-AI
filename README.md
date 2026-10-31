# Marine Biodiversity AI

Detecting deep-sea animals in underwater photos with computer vision, plus a look at where some of these species have been recorded (OBIS).

Built as a first computer vision project: data exploration, a YOLO11 object detector trained on a laptop CPU, a Streamlit demo, OBIS species maps and Grad-CAM heat maps.

## Results

The model was trained on the 20 most common animal types in FathomNet (1,970 images, split 80/10/10 into train, validation and test). Scores below are on the **held-out test set** (197 images, never used for training or model selection).

| Model | Classes | Test mAP50 | Precision | Recall |
| --- | --- | --- | --- | --- |
| YOLO11n, 40 epochs | 20 | 0.451 | 0.502 | 0.450 |
| YOLO11n, +20 epochs, sponge labels merged | 18 | **0.487** | 0.534 | 0.474 |

- mAP50 is the main detection score (0 to 1, higher is better). The model finds about half of the animals.
- It does best on large, distinctive animals (for example branching corals such as *Keratoisis* and fish such as *Anoplopoma*) and worst on small animals and sponges.
- The improvement from 0.451 to 0.487 comes from two changes at once: merging three overlapping sponge labels (`Porifera`, `sponge`, `Hexactinellida`) into one class, and 20 extra epochs of training. Their separate effects were not measured.
- Per-class scores are noisy, because many classes have only 10 to 60 test instances.

## What the project does

1. **Explore the data.** FathomNet annotations (COCO format): 119,096 images, 280,118 labelled animals, 1,897 animal types.
2. **Find the problem.** The data is long-tailed: 60 types have 1,000+ examples, but over half have fewer than 10.
3. **Build a smaller dataset.** The 20 most common animals, up to 100 images each (1,970 images), converted to YOLO format.
4. **Train and evaluate** a YOLO11 nano detector from pretrained weights (CPU only).
5. **Demo.** A Streamlit app: upload a photo, set a confidence level, see the detected animals.
6. **Biodiversity side.** OBIS occurrence records for selected species, plotted as longitude and latitude.
7. **Explain the model.** A simplified Grad-CAM heat map for the model's strongest guess in a photo.

## Project structure

```text
Marine-Biodiversity-AI/
├── dashboard/
│   └── app.py                      # Streamlit demo
├── scripts/
│   ├── inspect_json.py, peek_json.py, report.py, check_links.py   # look inside the annotation file
│   ├── top_animals.py              # class counts and chart
│   ├── download_images.py, download_subset.py, check_download.py  # fetch images via the FathomNet API
│   ├── draw_boxes.py               # draw annotation boxes to check labels
│   ├── make_subset.py              # top-20 subset
│   ├── make_yolo_dataset.py        # YOLO format + train/val/test split (20 classes)
│   ├── make_yolo_dataset_merged.py # same, with sponge labels merged (18 classes)
│   ├── train.py, train_merged.py   # training (settings were changed between runs)
│   ├── predict.py                  # predictions on the test images
│   ├── obis_map.py, obis_counts.py, obis_multi_map.py   # OBIS records
│   └── gradcam.py                  # Grad-CAM heat maps
├── README.md
├── requirements.txt
└── .gitignore
```

Datasets, images, training runs and outputs are not stored in this repository.

## How to reproduce

1. Create an environment (Python 3.11) and install the packages:
   ```bash
   pip install ultralytics pandas pillow matplotlib fathomnet streamlit
   ```
2. Get the FathomNet annotation files from [fathomnet.org](https://fathomnet.org) and place `train.json` in `datasets/fathomnet/annotations/`.
3. Build the subset and download its images:
   ```bash
   python scripts/make_subset.py
   python scripts/download_subset.py
   ```
4. Build the YOLO dataset and train:
   ```bash
   python scripts/make_yolo_dataset_merged.py
   python scripts/train_merged.py
   ```
5. Run the demo (after updating `MODEL_PATH` in `dashboard/app.py` to your trained `best.pt`):
   ```bash
   streamlit run dashboard/app.py
   ```

The trained weights are not included in this repository.

## Limitations

- Only 20 of the 1,897 animal types are covered.
- The model misses about half of the animals, especially small ones in dim water.
- Sponges remain one of the weakest classes even after merging.
- OBIS plots use the first 1,000 records returned per species, which is a sample and not the full range. Records show where scientists have looked, not how common a species is.
- The Grad-CAM implementation is simplified, and its maps are rough evidence, not proof of what the model "understands".

## Credits

- Images and annotations: [FathomNet](https://fathomnet.org) and MBARI. Please follow FathomNet's data use policy if you reuse the images.
- Species occurrence records: [OBIS](https://obis.org).
- Model: [Ultralytics YOLO11](https://github.com/ultralytics/ultralytics).
