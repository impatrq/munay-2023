import ultralytics
from ultralytics import YOLO

#%%

ultralytics.checks()

#%%

#path_model = r'projects/runs/segment/train/weights/best.pt'

#%%

#model = YOLO(path_model)
model = YOLO('yolov8s.pt')

#%%
#path_video = r'Tracker_Example/14-02_25_23-01_12_50-ID1_ID2_ID3_ID4.mp4'
#tracker = model.track(path_video, show=True)
results = model('https://static7.depositphotos.com/1313859/792/i/450/depositphotos_7920163-stock-photo-yellow-warbler-dendroica-petechia-singing.jpg')

results.show()