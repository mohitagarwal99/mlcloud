import cv2
cap = cv2.VideoCapture(0)
status, photo = cap.read()

allos = []
import boto3
ec2 = boto3.resource("ec2")


def myosLaunch():
        instances = ec2.create_instances(
            ImageId = "ami-0a2acf24c0d86e927",
            MinCount = 1,
            MaxCount=1,
            InstanceType="t2.micro",
            SecurityGroupIds = ["sg-0301b69eb9b4323ae"])
        myid = instances[0].id
        allos.append(myid)
        print("Total os:", len(allos))
        print(myid)
        
def myosTerminate():
    osdelete = allos.pop()
    ec2.instances.filter(InstanceIds = [osdelete]).terminate()
    print("total os:", len(allos))

#pip install cvzone
#pip install mediapipe

from cvzone.HandTrackingModule import HandDetector
detector = HandDetector(maxHands =1) #model given by media pipe used to detect hand

while True:
    status, photo = cap.read()
    cv2.imshow("my photo", photo)
    if cv2.waitKey(100) == 13:
        break
    hand = detector.findHands(photo, draw = False) # detector.findHands(photo, draw = False)

    if hand:
        lmlist = hand[0]
       # print(detector.fingersUp(lmlist))
        totalFinger = detector.fingersUp(lmlist)
        if totalFinger == [0, 1, 1, 0, 0]:
            print("Two fingers detected, launching OS...")
            myosLaunch()
        elif totalFinger == [0, 1, 0, 0, 0]:
            print("One finger detected, terminating OS...")
            myosTerminate()
        else:
            print("Don't know what to do")
cv2.destroyAllWindows()
 
cap.release()
