from PIL import Image


class ImageFileFeeder(object):
    def __init__(self):
        self.images = []
        self.images.append(Image.open('../data/haoyou/crop-20170706-045754.248068.jpg').resize((400, 400)))
        self.images.append(Image.open('../data/haoyou/crop-20170706-050022.691116.jpg').resize((400, 400)))
        self.images.append(Image.open('../data/zhaohuan/crop-20170706-045934.039165.jpg').resize((400, 400)))

    def feed(self):
        return self.images.pop()


class RealCaptureFeeder(object):
    def __init__(self, capture):
        self.capture = capture

    def feed(self):
        return self.capture.image()
