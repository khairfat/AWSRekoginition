import tkinter
import cv2
import PIL.Image
import PIL.ImageTk
import time
import cv2
import csv
import boto3
import pyttsx3
AWS_DEFAULT_REGION = 'us-west-2'


class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        self.vid = MyVideoCapture(self.video_source)
        self.canvas = tkinter.Canvas(
            window, width=self.vid.width, height=self.vid.height)
        self.canvas.pack()
        self.btn_snapshot = tkinter.Button(
            window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=tkinter.CENTER, expand=True)
        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()

        if ret:
            cv2.imwrite("frame" + ".jpg",
                        cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))
            engine = pyttsx3.init()
            photo = "frame.jpg"

            AWSAccessKeyId = ""
            AWSSecretKey = ""
            client = boto3.client('rekognition',
                                  region_name=AWS_DEFAULT_REGION,
                                  aws_access_key_id=AWSAccessKeyId,
                                  aws_secret_access_key=AWSSecretKey)

            with open(photo, 'rb') as source_image:
                source_bytes = source_image.read()

            response = client.detect_labels(
                Image={'Bytes': source_bytes},
                MaxLabels=10,
                MinConfidence=99
            )

            for label in response['Labels']:
                print(label['Name'])

            for label in response['Labels']:
                answer = label['Name']
                engine.say(answer)
                engine.runAndWait()

    def update(self):
        ret, frame = self.vid.get_frame()

        if ret:
            self.photo = PIL.ImageTk.PhotoImage(
                image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)

        self.window.after(self.delay, self.update)


class MyVideoCapture:
    def __init__(self, video_source=0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video source", video_source)

        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(tkinter.Tk(), "Tkinter and OpenCV")
