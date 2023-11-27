import rclpy
from rclpy.node import Node
from iqs_msgs.srv import ScanManuverability
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
import cv2
import numpy as np
import math
import mysql.connector

def average_color_around_point(image, center, radius):
    # Convert the image to the LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)

    # Create a mask for the circular region
    mask = np.zeros_like(image)
    cv2.circle(mask, center, radius, (255, 255, 255), thickness=cv2.FILLED)

    # Apply the mask to the LAB image
    masked_lab = cv2.bitwise_and(lab_image, mask)

    # Calculate the mean color in the circular region
    average_color_lab = np.mean(masked_lab, axis=(0, 1))

    # Convert the average color back to BGR
    average_color_bgr = cv2.cvtColor(np.uint8([[average_color_lab]]), cv2.COLOR_Lab2BGR)[0, 0]

    return average_color_bgr


def cursor_connection():
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="darkcyde15",
    database="IQS_2024"
    )
    cursor=mydb.cursor()
    return mydb, cursor

class Pylon:
    def __init__(self,x,y,angle,size,type):
        self.angle=angle
        self.x=x
        self.y=y
        self.size=size
        self.score=0
        self.type=type

    def __str__(self):
        return f"Pylon Type: {self.type} x: {self.x} y: {self.y} size: {self.size} angle: {self.angle} score: {self.score}"
    
    def upload(self,cursor):
        sql=f"INSERT INTO manuverability_track (type,x,y,angle,size) VALUES (%s, %s, %s, %s, %s)"
        vals=self.type,self.x,self.y,self.angle,self.size
        cursor.execute(sql,vals)
    
    

class PylonDetectionNode(Node):
    def __init__(self):
        super().__init__('pylon_detection_node')
        self.service = self.create_service(
            ScanManuverability, 'scan_manuverability', self.detect_pylons_callback)
        self.bridge = CvBridge()
        self.img_sub=self.create_subscription(Image,"manuverability_top_down",self.img_callback,10)
        self.image=Image()
        self.download()
        self.snapshot=np.zeros((512, 512, 3), np.uint8)
        self.diff_pub=self.create_publisher(Image,"man_diff",10)

        #print(self.pylons)

    
    def score(self):
        #cv_img=CvBridge.imgmsg_to_cv2(self.bridge,self.image)

        difference = cv2.absdiff(self.cv_image, self.snapshot)
        difference_gray = cv2.cvtColor(difference, cv2.COLOR_BGR2GRAY)
        self.diff_pub.publish(CvBridge.cv2_to_imgmsg(self.bridge,difference_gray))
        for i,pylon in enumerate(self.pylons):
            print(average_color_around_point(self.image,(pylon.x,pylon.y),10))
            #pylon.score=i




    def download(self):
        db,cursor=cursor_connection()
        self.pylons=[]
        sql="SELECT x,y,type,size,angle FROM manuverability_track"
        cursor.execute(sql)
        result = cursor.fetchall()
        for i in result:
            x,y,type,size,angle=i
            pylon=Pylon(x,y,angle,size,type)
            self.pylons.append(pylon)
            print(pylon)
        db.close()

    def img_callback(self,msg):
        self.image=msg
        self.cv_image = self.bridge.imgmsg_to_cv2(self.image, desired_encoding='bgr8')
        self.score()
    
    

    def detect_pylons_callback(self, request, response):
        try:
            # Convert ROS image message to OpenCV image
            #cv_image = self.bridge.imgmsg_to_cv2(self.image, desired_encoding='bgr8')
            self.snapshot=self.cv_image
            # Dummy pylon detection (replace this with your actual detection logic)
            pylons = self.detect_pylons(self.cv_image)

            # Fill the response with detection results
            response.pylons = len(pylons)
            #response.success = True

        except Exception as e:
            self.get_logger().error(f"Error detecting pylons: {str(e)}")
            #response.success = False

        return response

    def detect_pylons(self, cv_image):
        db,cursor=cursor_connection()
        sql="DELETE FROM manuverability_track"
        cursor.execute(sql)
        img=cv_image
        hsv_img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define the lower and upper bounds for yellow color in HSV
        lower_yellow = np.array([20, 100, 100])
        upper_yellow = np.array([30, 255, 255])

        # Create a mask for yellow pixels
        yellow_mask = cv2.inRange(hsv_img, lower_yellow, upper_yellow)

        # Find contours in the yellow mask
        contours, _ = cv2.findContours(yellow_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        yellow_rectangles = []
        red_rectangles = []
        self.pylons= []

        for contour in contours:
            # Approximate the contour with a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # If the polygon has four vertices, it's likely a rectangle
            if len(approx) == 4:
                # Draw the rectangle on the original image
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)

                # Calculate the angle of the rectangle
                rect = cv2.minAreaRect(contour)
                angle = rect[2]
                print(rect)
                pylon=Pylon(rect[0][0],rect[0][1],rect[2],((rect[1][0]+rect[1][1])/2),1)
                pylon.upload(cursor)
                self.pylons.append(pylon)
        
        lower_red = np.array([20, 20, 20])
        upper_red = np.array([30, 30, 255])
        red_mask=cv2.inRange(hsv_img, lower_yellow, upper_yellow)
        red_contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for contour in red_contours:
            # Approximate the contour with a polygon
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)

            # If the polygon has four vertices, it's likely a rectangle
            if len(approx) == 4:
                # Draw the rectangle on the original image
                cv2.drawContours(img, [approx], 0, (0, 255, 0), 2)

                # Calculate the angle of the rectangle
                rect = cv2.minAreaRect(contour)
                angle = rect[2]
                print(rect)
                pylon=Pylon(rect[0][0],rect[0][1],rect[2],((rect[1][0]+rect[1][1])/2),2)
                pylon.upload(cursor)
                self.pylons.append(pylon)
            

        db.commit()
        db.close()
        return self.pylons
        # Display the results
        #cv2.imshow('Yellow Rectangles', img)
        #cv2.imshow('Yellow Mask', yellow_mask)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
    


        

def main(args=None):
    rclpy.init(args=args)
    pylon_detection_node = PylonDetectionNode()
    rclpy.spin(pylon_detection_node)
    pylon_detection_node.destroy_node()
    cv2.destroyAllWindows()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
