import cv2
import face_recognition
import os
import pickle
import numpy as np
import pyttsx3
import threading
import logging
from datetime import datetime
from database.db import DatabaseManager
from ai.liveness import LivenessDetector


CONFIDENCE_THRESHOLD = 70
FACE_DISTANCE_THRESHOLD = 0.65


class FaceRecognizer:

    def __init__(self, model_path="models/encodings.pkl",
                 unknown_dir="unknown_faces"):

        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        self.model_path = os.path.join(base_dir, model_path)
        self.unknown_dir = os.path.join(base_dir, unknown_dir)

        self.db = DatabaseManager()
        self.liveness = LivenessDetector()


        if not os.path.exists(self.unknown_dir):
            os.makedirs(self.unknown_dir)


        self.known_encodings = []
        self.known_names = []
        self.known_ids = []


        self.session_marked_cache = set()
        self.unknown_logged_cache = set()


        self.load_model()


    # ---------------- LOAD MODEL ----------------

    def load_model(self):

        if os.path.exists(self.model_path):

            try:

                with open(self.model_path,"rb") as f:

                    data = pickle.load(f)

                    self.known_encodings = data["encodings"]
                    self.known_names = data["names"]
                    self.known_ids = data["ids"]

                print("Model loaded")

                return True


            except Exception as e:

                print(e)



        return False



    # ---------------- VOICE ----------------

    def speak(self,text):

        def run():

            engine = pyttsx3.init()

            engine.setProperty(
                "rate",
                145
            )

            engine.say(text)

            engine.runAndWait()


        threading.Thread(
            target=run,
            daemon=True
        ).start()



    # ---------------- CAMERA ----------------


    def run_recognition(self,camera_index=0,frame_callback=None):


        if not self.known_encodings:

            return False,"No trained model found"



        cap=cv2.VideoCapture(camera_index)


        if not cap.isOpened():

            return False,"Camera error"



        while True:


            ret,frame=cap.read()


            if not ret:
                break



            small=cv2.resize(
                frame,
                (0,0),
                fx=0.25,
                fy=0.25
            )


            rgb=cv2.cvtColor(
                small,
                cv2.COLOR_BGR2RGB
            )



            locations=face_recognition.face_locations(rgb)

            encodings=face_recognition.face_encodings(
                rgb,
                locations
            )



            for face_encoding,location in zip(
                    encodings,
                    locations):


                top,right,bottom,left=location


                top*=4
                right*=4
                bottom*=4
                left*=4



                distances=face_recognition.face_distance(
                    self.known_encodings,
                    face_encoding
                )


                name="Unknown"

                student_id=None

                confidence=0



                if len(distances)>0:


                    best=np.argmin(distances)

                    distance=distances[best]



                    confidence=(1-distance)*100



                    if distance < FACE_DISTANCE_THRESHOLD:

                        name=self.known_names[best]

                        student_id=self.known_ids[best]




                # ---------------- KNOWN FACE ----------------


                if name!="Unknown":


                    status="Checking..."

                    color=(0,255,0)



                    if confidence >= CONFIDENCE_THRESHOLD:


                        if student_id not in self.session_marked_cache:



                            success,msg=self.db.mark_attendance(
                                student_id,
                                name,
                                confidence
                            )


                            if success:


                                self.session_marked_cache.add(
                                    student_id
                                )


                                self.speak(
                                    f"Welcome {name}. Attendance marked"
                                )


                                status="Attendance Marked"



                            else:


                                status="Already Marked"



                        else:

                            status="Verified"



                    else:

                        status="Low Confidence"



                    cv2.rectangle(
                        frame,
                        (left,top),
                        (right,bottom),
                        color,
                        2
                    )


                    cv2.putText(
                        frame,
                        f"{name} {confidence:.1f}%",
                        (left,top-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )


                    cv2.putText(
                        frame,
                        status,
                        (left,bottom+25),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        color,
                        2
                    )




                # ---------------- UNKNOWN FACE ----------------


                else:


                    cv2.rectangle(
                        frame,
                        (left,top),
                        (right,bottom),
                        (0,0,255),
                        2
                    )


                    cv2.putText(
                        frame,
                        "Unknown Person",
                        (left,top-10),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.7,
                        (0,0,255),
                        2
                    )




            if frame_callback:

                frame_callback(frame)



            cv2.imshow(
                "SmartAttend AI",
                frame
            )



            if cv2.waitKey(1)&0xff==ord('q'):

                break



        cap.release()

        cv2.destroyAllWindows()


        return True,"Completed"





if __name__=="__main__":


    face=FaceRecognizer()

    face.run_recognition()