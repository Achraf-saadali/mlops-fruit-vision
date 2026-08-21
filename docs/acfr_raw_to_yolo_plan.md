# ACFR Data: Stage 01 Raw Ingestion and the Future YOLO Conversion

## Stage 01 scope: what has been implemented

Stage 01 preserves the original ACFR dataset. It does **not** modify images, rewrite CSV annotations, create YOLO labels, resize files, merge fruits, or change the official train/validation/test splits.

The expected original root is:

```text
acfr-fruit-dataset/
├── almonds/
│   ├── annotations/      # CSV: item,x,y,dx,dy,label
│   ├── images/           # 300 × 300 PNG images
│   ├── labelmap.json
│   └── sets/             # all, train, train_val, val, test split files
├── apples/
│   ├── annotations/      # CSV: item,c-x,c-y,radius,label
│   ├── images/           # 308 × 202 PNG images
│   ├── labelmap.json
│   ├── segmentations/    # Apple pixel-wise annotations
│   └── sets/
├── mangoes/
│   ├── annotations/      # CSV: item,x,y,dx,dy,label
│   ├── images/           # 500 × 500 PNG images
│   ├── labelmap.json
│   └── sets/
└── readme.txt
```

The remote Hugging Face destination configured in `config/config.yaml` is:

```text
ACH-2003/acr_fruit
└── acfr/
    └── raw/
        └── acfr-fruit-dataset/
```

## Why Stage 01 does not create a YOLO dataset

The raw annotation formats differ by fruit. The converter must be written only after inspecting actual CSV rows and `labelmap.json` files. Stage 01 first gives every environment an identical, untouched source copy.

| Fruit subset | ACFR annotation shape | Future YOLO conversion |
|---|---|---|
| `almonds` | Rectangle: `x, y, dx, dy` | Convert top-left coordinates and width/height to YOLO center/width/height, normalized by image size. |
| `mangoes` | Rectangle: `x, y, dx, dy` | Same rectangle-to-YOLO conversion. |
| `apples` | Circle: `center_x, center_y, radius` | Convert the circle to enclosing box: `x=center_x-radius`, `y=center_y-radius`, `w=2r`, `h=2r`, then normalize. |

A future Stage 03 transformer should produce a **separate** directory:

```text
artifacts/data_transformation/acfr_yolo_detection_v1/
├── images/
│   ├── train/
│   ├── val/
│   └── test/
├── labels/
│   ├── train/
│   ├── val/
│   └── test/
└── data.yaml
```

The original raw directory must never be overwritten.

## How the official splits are used later

The future transformer reads the existing ACFR split lists, for example:

```text
almonds/sets/train.txt
almonds/sets/val.txt
almonds/sets/test.txt
```

It copies or links each original image to the matching YOLO split and writes a same-named `.txt` label file. It must not create a random split, because the source provides official split lists.

## What must be inspected before Stage 03

Use `research/trials.ipynb` only for inspection and visualization. Verify these items with real files:

1. The exact CSV column order and whether image identifiers include `.png`.
2. Whether every image has a matching annotation CSV.
3. The contents of each `labelmap.json`.
4. Whether the rectangle values are already in pixel coordinates.
5. Whether the source split files contain base names, relative paths, or filenames with extensions.
6. Whether your first YOLO model should use one class, `fruit`, or three classes, `almond`, `apple`, and `mango`.

Only after that inspection should `components/data_transformation.py` be implemented.
