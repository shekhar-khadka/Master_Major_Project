import time
from pathlib import Path

import cv2
import torch
import torch.backends.cudnn as cudnn
from numpy import random
import numpy as np

from models.experimental import attempt_load
from utils.datasets import LoadStreams, LoadImages,letterbox
from utils.general import check_img_size, check_requirements, check_imshow, non_max_suppression, apply_classifier, \
    scale_coords, xyxy2xywh, strip_optimizer, set_logging, increment_path
from utils.plots import plot_one_box
from utils.torch_utils import select_device, load_classifier, time_synchronized, TracedModel


class DetectFrames:
    def __init__(self,weight,conf,img_size,device,conf_thres,iou_thres):
        self.weights = weight
        self.conf = conf
        self.device = device
        self.img_size = img_size[0]
        self.conf_thres = conf_thres
        self.iou_thres = iou_thres
        self.pre_model = attempt_load(self.weights, map_location=self.device)  # load FP32 model
        self.stride = int(self.pre_model.stride.max())
        self.model = TracedModel(self.pre_model, self.device, self.img_size)

        self.device = device

    def detect(self,source):
        # print(source)
        device = self.device
        half = device.type != 'cpu'

        #load model
        # model = attempt_load(self.weights, map_location=device)  # load FP32 model
        # stride = int(model.stride.max())  # model stride
        imgsz = check_img_size(self.img_size, s=self.stride)  # check img_size



        if half:
            self.model.half()  # to FP16
        vid_path, vid_writer = None, None


        # Get names and colors
        names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        colors = [[random.randint(0, 255) for _ in range(3)] for _ in names]

        # Run inference
        if device.type != 'cpu':
            self.model(torch.zeros(1, 3, imgsz, imgsz).to(device).type_as(next(self.model.parameters())))  # run once
        old_img_w = old_img_h = imgsz
        old_img_b = 1
        t0 = time.time()
        #         dataset = LoadImages(source, img_size=imgsz, stride=self.stride)

        img0 = source
        img = letterbox(img0, imgsz, stride=self.stride)[0]
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)




        # for path, img, im0s, vid_cap in dataset:
        img = torch.from_numpy(img).to(device)
        img = img.half() if half else img.float()  # uint8 to fp16/32
        img /= 255.0  # 0 - 255 to 0.0 - 1.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        #warmup
        if device.type != 'cpu' and (
                old_img_b != img.shape[0] or old_img_h != img.shape[2] or old_img_w != img.shape[3]):
            old_img_b = img.shape[0]
            old_img_h = img.shape[2]
            old_img_w = img.shape[3]
            for i in range(3):
                self.model(img, augment=None)[0]

        t1 = time_synchronized()
        with torch.no_grad():   # Calculating gradients would cause a GPU memory leak
            pred = self.model(img, augment=False)[0]
        t2 = time_synchronized()

    # Apply NMS
        pred = non_max_suppression(pred, self.conf_thres, self.iou_thres, classes=None, agnostic=False)
        t3 = time_synchronized()


        # Process detections
        for i, det in enumerate(pred):  # detections per image
            s, im0, frame = '%g: ' % i, img0, 1
            # gn = torch.tensor(im0.shape)[[1, 0, 1, 0]]  # normalization gain whwh
            if len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0.shape).round()

                # Print results
                for *xyxy, conf, cls in reversed(det):
                    label = f'Detected {names[int(cls)]} with  {conf:.2f}'
                    plot_one_box(xyxy, im0, label=label, color=colors[int(cls)], line_thickness=1)
                    print(label)
                    # print(f'{s}Detected with conf {conf:.2f} in ({(1E3 * (t2 - t1)):.1f}ms)')

                    cv2.imshow('OK', im0)
                    k = cv2.waitKey(1)  # 1 millisecond

            # cv2.imshow(str(p), im0)
            # k = cv2.waitKey(1)  # 1 millisecond
            # if k == ord('q'):
            #     break

        # print(f'Done. ({time.time() - t0:.3f}s)')


# if __name__ == '__main__':
#     image_source='1225.jpg'
#     conf=0.5
#     img_size=640,
#     device='cpu'
#     weight='best.pt'
#     conf_thres=0.25
#     iou_thres=0.45
#
#
#     obj=DetectFrames(image_source,weight,conf,img_size,device,conf_thres,iou_thres)
#     obj.detect()
