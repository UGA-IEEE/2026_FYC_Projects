import os
import json
import requests

# ---------- CONFIG ----------
LS_URL = "http://localhost:8080"      # same URL you open in browser
PROJECT_ID = 0                        # your actual project ID in the URL /projects/<id>/
PAT = "your_personal_access_token_here"  # create in Label Studio UI

FROM_NAME = "component"   # must match <Choices name="component"...> in your labeling config
TO_NAME   = "image"       # must match <Image name="image"...> in your labeling config

PRED_FILE = "predictions_for_labelstudio.json"


def normalize_name(name: str) -> str:
    """
    Turn things like:
      'upload/3/f491dfba-img_9467.jpg' -> 'img_9467.jpg' (lowercase)
      'dataset/IMG_9467.JPG'          -> 'img_9467.jpg' (lowercase)
    """
    base = os.path.basename(name).strip().lower()
    if "-" in base:
        base = base.split("-", 1)[1]  # drop random hash prefix before first '-'
    return base


# 1. use PAT to get short-lived access token
refresh_resp = requests.post(
    f"{LS_URL}/api/token/refresh",
    headers={"Content-Type": "application/json"},
    data=json.dumps({"refresh": PAT})
)
if refresh_resp.status_code != 200:
    raise RuntimeError(f"Failed to get access token: {refresh_resp.status_code} {refresh_resp.text}")

ACCESS_TOKEN = refresh_resp.json()["access"]
auth_headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}
print("[OK] Got access token")


# 2. load CLIP predictions from disk
with open(PRED_FILE, "r") as f:
    clip_preds_raw = json.load(f)

print(f"[OK] Loaded {len(clip_preds_raw)} model predictions from {PRED_FILE}")

# build lookup: normalized filename -> predicted label
pred_by_normname = {}
for p in clip_preds_raw:
    img_path = p["image"]            # e.g. dataset/IMG_9467.JPG
    predicted_label = p["predicted_label"]  # e.g. "GPU"
    norm = normalize_name(img_path)  # -> img_9467.jpg
    pred_by_normname[norm] = predicted_label


# 3. pull all tasks from the project
tasks_resp = requests.get(
    f"{LS_URL}/api/projects/{PROJECT_ID}/tasks",
    headers=auth_headers,
)
if tasks_resp.status_code != 200:
    raise RuntimeError(f"Failed to get tasks: {tasks_resp.status_code} {tasks_resp.text}")

raw = tasks_resp.json()

if isinstance(raw, list):
    tasks = raw
elif isinstance(raw, dict) and "results" in raw:
    tasks = raw["results"]
elif isinstance(raw, dict):
    tasks = [raw]
else:
    raise TypeError(f"Unexpected tasks payload type: {type(raw)}")

print(f"[OK] Project returned {len(tasks)} tasks")


# 4. loop tasks, match prediction, POST to /api/predictions
matches = 0

for t in tasks:
    if not isinstance(t, dict):
        continue
    if "id" not in t or "data" not in t:
        continue

    task_id = t["id"]
    img_field = t["data"].get("image", "")

    # normalize task filename like f491dfba-img_9467.jpg -> img_9467.jpg
    norm_task_name = normalize_name(img_field)

    if norm_task_name not in pred_by_normname:
        print(f"[WARN] No CLIP prediction for {norm_task_name}, skipping")
        continue

    predicted_label = pred_by_normname[norm_task_name]
    print(f"[PUSH] Task {task_id} ({norm_task_name}) -> {predicted_label}")

    prediction_payload = {
        "task": task_id,
        "model_version": "clip_bootstrap",
        "score": 0.5,  # dummy confidence
        "result": [
            {
                "from_name": FROM_NAME,
                "to_name": TO_NAME,
                "type": "choices",
                "value": {
                    "choices": [predicted_label]
                }
            }
        ],
    }

    pr = requests.post(
        f"{LS_URL}/api/predictions",
        headers=auth_headers,
        data=json.dumps(prediction_payload)
    )

    if pr.status_code not in (200, 201):
        print(f"[ERR] Failed task {task_id}: {pr.status_code} {pr.text[:200]}")
    else:
        print(f"[OK] Attached prediction to task {task_id}")
        matches += 1

print(f"[DONE] Attached predictions to {matches} tasks")
