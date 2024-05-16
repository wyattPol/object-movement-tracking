'''
create by   wyattPol
This can be used to track movement objects
'''
import cv2
cap = cv2.VideoCapture(0) 

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

ret, frame1 = cap.read()
ret, frame2 = cap.read()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    diff = cv2.absdiff(frame1, frame2)  
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (5, 5), 0) 
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)  
    dilated = cv2.dilate(thresh, None, iterations=5)  
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  

    if contours: #only track the biggest one
        largest_contour = max(contours, key=cv2.contourArea)  

        (x, y, w, h) = cv2.boundingRect(largest_contour) 
        if cv2.contourArea(largest_contour) > 900:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame1, "Status: {}".format('Movement'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX,
                        1, (0, 0, 255), 3)  

    cv2.imshow("Motion Detection", frame1)

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
