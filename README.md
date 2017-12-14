# Class-Availability-Notifier

<img src="images/Class-notifier.png" alt="Notifier" >

Automatically sends you a notification via Sound or Text when a class you're looking for is available. Only works for the University of South Florida

### How-to
-----
1. Enter class CRN
2. Select Term
3. Select Campus
4. Hit "Lookup Class"
5. Program will refresh the page every 60 seconds. A whistle sound will play if the class has seats open. A low beep will play to let you know that it found your class but no seats are open. I suggest just leaving the application in the background.
  
### Setting up text messaging
-----
  > Text messaging will require you to have a Twilio account, it's a text messaging api. 
  > Register a free account, get your Account SID and API key. Then Register a new number, after you register a new number click on it and add your personal phone number to the list numbers your twilio from number can send messages too.
 
<img src="images/texting.png" alt="texting" >
 
  Then go to tools > API keys > Create New API Key > Name it and Create API Key > Copy down your phone number API secret as you only see it once! > Paste your Account SID, API key, and Secret key into the app along with your from number and to number **no dashes**
  
  To not waste your text messages the notifier will only send the text once and only once when your class is available. Restart the application to reset text messaging.
