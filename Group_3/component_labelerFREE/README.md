i built a fully local, free auto labeling system for electronics components like ram, cpu, gpu, usb_drive using open source tools like: (tried to use openai chatgpt llm, but ts cost money)

Label studio
CLIP (Open-CLIP/Hugging Face) - for image-level label bootstrapping
yolov11 (Ultralytics) - for bounding box object detection
Python scripts - for integrating and automating the entire process.

-1 setup -
took and organized 100+ photos of components
installed and ran Label studio locally.

-2 auto labeling with CLIP
Goal: auto-assign a probable class (RAM/CPU/GPU/USB_Drive) to each image.

How it worked: the script loaded a pretrained ViT-B/32CLIP model locally. For each image, it compared visual embeddings with text prompts:
"a photo of a CPU", "a photo of a RAM stick", "a photo of a GPU", "a photo of a USB drive".
It assigned the label with the highest cosine similarity.
output example: 
[
  {"image": "dataset/img_001.jpg", "predicted_label": "GPU"},
  {"image": "dataset/img_002.jpg", "predicted_label": "RAM"}
]
[
  {"image": "dataset/img_001.jpg", "predicted_label": "GPU"},
  {"image": "dataset/img_002.jpg", "predicted_label": "RAM"}
]
No API Calls. 100% offline. (ITS FREE)


Opened each image inside Label Studio.

Verified / corrected the auto label.

Saved.

This built your verified classification dataset — still no paid API, everything local.

TL;DR - this automation worked but it didn't label the boxes for classification on LabelStudio. It is still highly WIP