###
# Run this file just only when it has updated user image on the Images folder
###

import os
import cv2
import face_recognition
import pickle

# Encode Images one-by-one
# Add into list one-by-one

# Import the 'Student' Images into the list
folderPath = 'Images'
pathList = os.listdir(folderPath)
imgList = []
studentIds = []
for path in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, path)))
    # print(os.path.splitext(path)[0]) # ('6388176', '.jpg')
    studentIds.append(os.path.splitext(path)[0])
print("Encoded Images:", studentIds)

# Encode Images
def findEncoding(imagesList):
    encodeList = []
    for img in imagesList:
        # Convert BGR (opencv) to RGB (face-recog)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList

if __name__ == "__main__":
    print(f"====================\nEncoding Started...")
    encodeListKnown = findEncoding(imgList)
    # Map Encoding lists with Ids
    encodeListKnownWithIds = [encodeListKnown, studentIds]
    print("Encoding Completed!")

    # Map Encoding lists with Ids into the file (write)
    file = open("EncodeFile.p", "wb")
    pickle.dump(encodeListKnownWithIds, file)
    file.close()
    print(f"File Saved =)\n====================")