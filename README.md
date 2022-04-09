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

---

<br/>
Counting Project Description:

Using the hand detector module in our project to detect the 0 to 21 landmarks on each hand and then with an IF loop we will detect which hand [Right / Left ] are up and then compare the highest landmark in each finger with some landmark in that finger if the highest landmark was upper than it the finger is open and otherwise the finger is close. For THUMB it is a little different because we could not compare the highest landmark in the vertical direction so we should detect the highest point located on which side of the lower point [Right / Left ] and then use this data and the hand side to detect in THUMB open or closed.
Finally, the results appending to a list, and then other parts of the program use simply this value in this list to show the picture or number.
