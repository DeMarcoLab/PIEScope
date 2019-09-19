"""Module for the Basler fluorescence detector."""

from pypylon import pylon


class Basler():
    def __init__(self):
        super(Basler, self).__init__()
        self.camera = pylon.InstantCamera(
            pylon.TlFactory.GetInstance().CreateFirstDevice())
        print("Using device ", self.camera.GetDeviceInfo().GetModelName())

        self.camera.MaxNumBuffer = 5
        self.imageCount = 1
        self.currentImageIndex = 0
        self.image = []

    def camera_grab(self):
        self.camera.Open()
        self.camera.StartGrabbingMax(self.imageCount)
        self.image = []

        while self.camera.IsGrabbing():
            grabResult = self.camera.RetrieveResult(
                5000, pylon.TimeoutHandling_ThrowException)

            if grabResult.GrabSucceeded():
                # print("SizeX: ", grabResult.Width)
                # print("SizeY: ", grabResult.Height)
                self.image = grabResult.Array
            else:
                print("Error: ", grabResult.ErrorCode,
                      grabResult.ErrorDescription)
            grabResult.Release()
        self.camera.Close()

        return self.image
