# REF: https://github.com/CHAITron/Youtube_Tutorials/blob/master/face_recog.py
# import face_recognition as face
# import numpy as np
# import cv2

# # Process video / Web cam
# video_capture = cv2.VideoCapture("test_vid.mp4")

# # Prepare image & encode face out
# cake_image = face.load_image_file("images/cake.png")
# cake_face_encoding = face.face_encodings(cake_image)[0]

# mueng_image = face.load_image_file("images/mueng.png")
# mueng_face_encoding = face.face_encodings(mueng_image)[0]

# face_locations = []
# face_encodings = []
# face_names = []
# face_percent = []
# # For calculating frame and frame+2
# process_this_frame = True

# known_face_encodings = [cake_face_encoding, mueng_face_encoding]
# known_face_names = ["CAKETHY", "MUENG"]

# # Calculate each frame
# while True:
#     # ret: successfully read or not
#     # frame: image extracted from each frame
#     ret, frame = video_capture.read()
#     if ret:
#         # Reduce processing time (reduce frame 2x)
#         small_frame = cv2.resize(frame, (0, 0), fx = 0.5, fy = 0.5)
#         # Convert BGR to RGB
#         rgb_small_frame = small_frame[:, :, ::-1]

#         if process_this_frame:
#             face_locations = face.face_locations(rgb_small_frame, model = "cnn")
#             face_encodings = face.face_encodings(rgb_small_frame, face_locations)
#             # Comparing face euclidean distance
#             for face_encoding in face_encodings:
#                 face_distances = face.face_distance(known_face_encodings, face_encoding)
#                 best = np.argmin(face_distances)
#                 face_percent_value = 1 - face_distances[best]
#                 # Match > 50 percent, show name
#                 if face_percent_value >= 0.5:
#                     name = known_face_names[best]
#                     percent = round(face_percent_value * 100, 2)
#                     face_percent.append(percent)
#                 else:
#                     name = "UNKNOWN"
#                     face_percent.append(0)
#                 face_names.append(name)

#         # Adjust showing element
#         for(top, right, bottom, left), name, percent in zip(face_locations, face_names, face_percent):
#             top *= 2
#             right *= 2
#             bottom *= 2
#             left *= 2
#             if name == "UNKNOWN":
#                 color = [46, 2, 209]
#             else:
#                 color = [255, 102, 51]
#             cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
#             cv2.rectangle(frame, (left - 1, top - 30), (right + 1,top), color, cv2.FILLED)
#             cv2.rectangle(frame, (left - 1, bottom), (right + 1,bottom + 30), color, cv2.FILLED)
#             font = cv2.FONT_HERSHEY_DUPLEX
#             cv2.putText(frame, name, (left + 6, top - 6), font, 0.6, (255, 255, 255), 1)
#             cv2.putText(frame, "MATCH: " + str(percent) + "%", (left + 6, bottom + 23), font, 0.6, (255, 255, 255), 1)
        
#         process_this_frame = not process_this_frame

#         # Show time (ms)
#         cv2.imshow("Video", frame);
#         if cv2.waitKey(100000) & 0xFF == ord('q'):
#             break
#     else:
#         print("Not successfully read, try again")
#         break