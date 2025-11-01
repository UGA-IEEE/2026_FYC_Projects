import os
import json
from pathlib import Path
from PIL import Image
import torch
from transformers import CLIPProcessor, CLIPModel

# ---------------- CONFIG ----------------
IMAGES_DIR = "dataset"   # folder with your images
LABELS = ["RAM", "CPU", "USB_Drive", "GPU", "Unknown"]
OUTPUT_JSON = "predictions_for_labelstudio.json"
CONFIDENCE_THRESHOLD = 0.3

print("=== STEP 0: environment check ===")
print("Python executable:", os.sys.executable)
print("Current working dir:", os.getcwd())

# ---------------- CHECK DATA FOLDER ----------------
dataset_path = Path(IMAGES_DIR)
print(f"=== STEP 1: checking images in {dataset_path.resolve()} ===")

if not dataset_path.exists():
    raise RuntimeError(f"FATAL: Folder '{IMAGES_DIR}' does not exist. Create it and put images there.")

image_paths = sorted([p for p in dataset_path.glob("*.*") if p.suffix.lower() in [".jpg", ".jpeg", ".png"]])
print(f"Found {len(image_paths)} candidate images:")
for p in image_paths[:5]:
    print("  sample ->", p)

if len(image_paths) == 0:
    raise RuntimeError("FATAL: No .jpg/.jpeg/.png images found in dataset/. Put your component photos there.")

# ---------------- LOAD CLIP ----------------
print("=== STEP 2: loading CLIP model ===")
device = "cuda" if torch.cuda.is_available() else "cpu"
print("Using device:", device)

model_name = "openai/clip-vit-base-patch32"
print("Loading model:", model_name, "... this can take a minute on first run")

model = CLIPModel.from_pretrained(model_name).to(device)
processor = CLIPProcessor.from_pretrained(model_name)

print("Model loaded OK.")

# ---------------- CLASSIFIER FUNCTION ----------------
def score_image(image_path, labels):
    img = Image.open(image_path).convert("RGB")
    # build natural language prompts for each label
    texts = [f"a photo of {lbl.replace('_', ' ').lower()}" for lbl in labels]
    inputs = processor(text=texts, images=img, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        outputs = model(**inputs)
        logits_per_image = outputs.logits_per_image  # shape [1, num_labels]
        probs = logits_per_image.softmax(dim=1).cpu().numpy()[0]
    return probs  # list of probabilities per label

# ---------------- RUN PREDICTIONS ----------------
print("=== STEP 3: running classification on images ===")
predictions = []

for idx, p in enumerate(image_paths):
    print(f"[{idx+1}/{len(image_paths)}] scoring {p.name} ...")
    probs = score_image(str(p), LABELS[:-1])  # exclude "Unknown" from direct scoring
    top_idx = int(probs.argmax())
    top_label = LABELS[top_idx]
    top_prob = float(probs[top_idx])

    if top_prob < CONFIDENCE_THRESHOLD:
        chosen = "Unknown"
    else:
        chosen = top_label

    reason = f"score={top_prob:.2f} for {chosen}"

    predictions.append({
        "task_path": str(p),
        "image": str(p),
        "predicted_label": chosen,
        "reason": reason
    })

print("=== STEP 4: saving predictions ===")
with open(OUTPUT_JSON, "w") as f:
    json.dump(predictions, f, indent=2)

print(f"Done. Wrote {OUTPUT_JSON}")
print("First 3 predictions:")
print(json.dumps(predictions[:3], indent=2))
print("=== COMPLETE ===")
