import PIL.ImageTk
import PIL.Image
import boto3
import pyttsx3
AWS_DEFAULT_REGION = 'us-west-2'

try:
    from Tkinter import *
    import tkFileDialog as filedialog
except ImportError:
    from tkinter import *
    from tkinter import filedialog


class App(Frame):
    def chg_image(self):
        if self.im.mode == "1":
            self.img = PIL.ImageTk.BitmapImage(self.im, foreground="white")
        else:
            self.img = PIL.ImageTk.PhotoImage(self.im)
        self.la.config(image=self.img, bg="#000000",
                       width=self.img.width(), height=self.img.height())

    def open(self):
        self.filename = filedialog.askopenfilename()
        if self.filename != "":
            self.im = PIL.Image.open(self.filename)
        self.chg_image()
        self.num_page = 0
        self.num_page_tv.set(str(self.num_page+1))

    def aws_process(self):
        engine = pyttsx3.init()
        AWSAccessKeyId = ""
        AWSSecretKey = ""
        client = boto3.client('rekognition',
                              region_name=AWS_DEFAULT_REGION,
                              aws_access_key_id=AWSAccessKeyId,
                              aws_secret_access_key=AWSSecretKey)

        with open(self.filename, 'rb') as source_image:
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

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master.title('Image Viewer')

        self.num_page = 0
        self.num_page_tv = StringVar()

        fram = Frame(self)
        Button(fram, text="Open File", command=self.open).pack(side=LEFT)

        Button(fram, text="Process", command=self.aws_process).pack(side=LEFT)
        Label(fram, textvariable=self.num_page_tv).pack(side=LEFT)
        fram.pack(side=TOP, fill=BOTH)

        self.la = Label(self)
        self.la.pack()

        self.pack()


if __name__ == "__main__":
    app = App()
    app.mainloop()
