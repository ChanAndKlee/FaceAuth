import tkinter as tk
import util
import cv2
from PIL import Image, ImageTk
import pickle
import numpy as np
import face_recognition
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime

# Connect to Firebase
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://facelogin-5c710-default-rtdb.firebaseio.com/",
})

class App:
    # Load the encoding file
    # Generated from: EncodeGenerator.py
    def load_encoding_file(self):
        print(f"====================\nLoading Encode File...")
        self.file = open('EncodeFile.p', 'rb')
        self.encodeListKnownWithIds = pickle.load(self.file)
        self.file.close()
        self.encodeListKnown, self.studentIds = self.encodeListKnownWithIds
        print("Encode File Loaded\n====================")
        return self.encodeListKnown, self.studentIds

    def __init__(self):
        # Call the encoding file
        self.encodeListKnown, self.studentIds = self.load_encoding_file()

        ### --- Main Page --- ###
        self.main_window = tk.Tk()
        self.main_window.title("FaceAuth - Login Page")
        self.main_window.geometry("1280x720+200+100")

        # Background
        self.background = tk.PhotoImage(file='Resources/background.png')
        self.label1 = tk.Label(self.main_window, image=self.background)
        self.label1.place(x=0, y=0)

        # Log in button
        self.login_btn_img = tk.PhotoImage(file='Resources/login_button.png')
        self.login_btn = tk.Button(self.main_window, image=self.login_btn_img,
                                   command=self.login, borderwidth=0, background='white')
        self.login_btn.pack(pady=30)
        self.login_btn.place(x=930, y=300)

        # Webcam frame label
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=50, y=160, width=700, height=500)

        # Add webcam to the webcam label
        self.add_webcam(self.webcam_label)

    def start(self):
        self.main_window.mainloop()

    ### --- Video Capturing --- ###
    def add_webcam(self, label):
        # If the webcam isnt created then create it
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(0)
        self._label = label
        self.process_webcam()

    def process_webcam(self):
        success, frame = self.cap.read()

        # Green square (Start-left, Start-top) (End-right, End-bottom)
        frame = cv2.rectangle(frame, (150, 75), (450, 400),
                              (0, 255, 0), thickness=3)

        if success == False:
            print("Webcam cannot be opened")

        self.most_recent_capture_arr = frame
        # Convert the webcam color before displaying on the screen
        img_ = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)

        # Keep repeating after 20ms (streaming)
        self._label.after(20, self.process_webcam)

    def login(self):
        ### --- Authentication --- ###
        imgS = cv2.resize(self.most_recent_capture_arr,
                          (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(self.most_recent_capture_arr, cv2.COLOR_BGR2RGB)

        faceCurFrame = face_recognition.face_locations(imgS)
        encodeCurFrame = face_recognition.face_encodings(imgS, faceCurFrame)

        counter = 0

        if faceCurFrame:
            for encodeFace in encodeCurFrame:
                self.matches = face_recognition.compare_faces(
                    self.encodeListKnown, encodeFace)
                self.faceDis = face_recognition.face_distance(
                    self.encodeListKnown, encodeFace)
                print("matches", self.matches)
                print("faceDis", self.faceDis)

                matchIndex = np.argmin(self.faceDis)
                print("Match Index", matchIndex)

                if self.matches[matchIndex]:
                    # Set new threshold leads to more accurate result
                    if self.faceDis[matchIndex] < 0.45:
                        id = self.studentIds[matchIndex]
                        if counter == 0:
                            counter = 1
                    else:
                        util.msg_box("Authentication Failed",
                                     "The user doesn't exist!")
                else:
                    util.msg_box("Authentication Failed",
                                 "The user doesn't exist!")

            if counter != 0:
                if counter == 1:
                    # Get the Data
                    studentInfo = db.reference(f'Students/{id}').get()
                    print(f"====================\nRetrieved: {studentInfo}")
                    print("====================")

                    util.msg_box("User Authenticated",
                                 f"User ID{id} is authenticated!")
                    self.main_window.destroy()

                    # Update data of attendance
                    ref = db.reference(f'Students/{id}')
                    ref.child('last_authenticated').set(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

                    ### --- User Page --- ###
                    logged_in_window = tk.Tk()
                    logged_in_window.title("FaceAuth - User Page")
                    logged_in_window.geometry("600x600+600+200")
                    logged_in_window.config(bg='black')

                    # Background
                    background = tk.PhotoImage(file='Resources/background.png')
                    label1 = tk.Label(logged_in_window, image=background)
                    label1.place(x=0, y=0)

                    # User Image
                    canvas = tk.Canvas(
                        logged_in_window, bg='black', width=300, height=300, highlightthickness=0)
                    canvas.place(relx=0.5, rely=0.5, anchor='center')

                    img_path = f"Images/{id}.jpg"
                    user_img = ImageTk.PhotoImage(Image.open(img_path))
                    canvas.create_image(150, 150, image=user_img)

                    label2 = tk.Label(logged_in_window,
                                      text=f"Hello, {studentInfo['name']}")
                    label2.config(font=("Poppins", 16))
                    label2.place(x=300, y=500, anchor='center')

                    logged_in_window.mainloop()
        else:
            util.msg_box("Fail Authenticated", "Cannot find the user's face!")


if __name__ == "__main__":
    app = App()
    app.start()