import torch

model = torch.hub.load('ultralytics/yolov5', 'yolov5s', force_reload=True)
im = 'https://static7.depositphotos.com/1313859/792/i/450/depositphotos_7920163-stock-photo-yellow-warbler-dendroica-petechia-singing.jpg'
results = model(im)
ave = 'bird'

if isinstance(results, torch.Tensor):
    print("El objeto results es un tensor y no es iterable")
else:
    if ave in results.pandas().xyxy[0]['name'].tolist():
        print("El string contiene la palabra")
    else:
        print("El string no contiene la palabra")


results.save()
results.print()
