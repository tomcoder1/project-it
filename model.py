from transformers import AutoImageProcessor, SiglipForImageClassification
from PIL import Image
import torch

model_name = "prithivMLmods/Food-101-93M"
processor = AutoImageProcessor.from_pretrained(model_name)
model = SiglipForImageClassification.from_pretrained(model_name)

def classify_food(path):
    try:
        img = Image.open(path).convert("RGB").resize((224, 224))  # Resize to model input size
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

    inputs = processor(images=img, return_tensors="pt")

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.softmax(logits, dim=1).squeeze()
    top5 = torch.topk(probs, k=5)

    top_label = model.config.id2label[int(top5.indices[0])]
    confidence = float(top5.values[0])
    return top_label, confidence
