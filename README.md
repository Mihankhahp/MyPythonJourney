# MyPythonJourney

Hand Tracking project
<br/>
Hand Tracking Land Marks
<br/>
![hand_landmarks](https://user-images.githubusercontent.com/85022016/161560591-df4909b0-3e19-4697-8e0e-c2e8bdd1b42f.png)
<br/><br/><br/>

---

<br/><br/><br/>
Pose Estimating Project
<br/>
Pose Estimate Land Marks;
<br/>
<br/>
![pose_tracking_full_body_landmarks](https://user-images.githubusercontent.com/85022016/161560953-550125c1-a4f6-405b-b5b6-509f5a26fce3.png)
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>

---

<br/>
Counting Project Description:

Using the hand detector module in our project to detect the 0 to 21 landmarks on each hand and then with an IF loop we will detect which hand [Right / Left ] are up and then compare the highest landmark in each finger with some landmark in that finger if the highest landmark was upper than it the finger is open and otherwise the finger is close. For THUMB it is a little different because we could not compare the highest landmark in the vertical direction so we should detect the highest point located on which side of the lower point [Right / Left ] and then use this data and the hand side to detect in THUMB open or closed.
Finally, the results appending to a list, and then other parts of the program use simply this value in this list to show the picture or number.

<br/>

---

<br/>
<br/>
<br/>
<br/>
<br/>

Personal Trainer Project

In this Project, we using the PoseEstimation module to figure out "findPose", "getPosition", and a new future which is added in this project "findAngle" which is totally dynamic in finding point's coordinate and drawing a line between them, and you could enter how many points you want. But we could find the angle between two lines and three points.
In the next step as in past projects, we set some visualization and then use our data to find out how many times the particular activity happened.
<br/>

---

<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
AL VIRTUAL PAINTER

In this program fingers' landmarks to define the exact coordinates of the fingers and then put if for Selecting or Drawing mode, followed by that we set some other if roots for each color and finally eraser.
<bt/>  
ultimately, we change the img type and show the changes on the final img .
<bt/>  
<bt/>  
<bt/>

    1.  Import img

<bt/>  
    2.Find Hands Landmarks
<bt/>  
    3.Check which fingers are up
<bt/>  
    4.If Selection Mode:==>
<bt/>  
    5.If Drawing Mode:==>
<bt/>
