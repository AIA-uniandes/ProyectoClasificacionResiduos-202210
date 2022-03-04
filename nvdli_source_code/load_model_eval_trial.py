import cv2
from utils import preprocess
import torch.nn.functional as F


model = torchvision.models.resnet18(pretrained=True)
model.fc = torch.nn.Linear(512, output_dim)
model = model.to(device)
model.load_state_dict(torch.load('/nvdli-nano/data/regression/bag_color_trial1.pth'))

cam = VideoCapture(0)
result, image = cam.read()
preprocessed = preprocess(image)
output = model(preprocessed)
output = model(preprocessed).detach().cpu().numpy().flatten()
print(output)
