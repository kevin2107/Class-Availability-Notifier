from pygame import mixer as notify
from time import sleep
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
import wx #GUI
import wx.adv#Advanced GUI Options
from twilio.rest import Client #text support
#Test CRN: 24345

Current = '0.9.6'
'''	
	Todo:Save twilio-API settings +0.0.1
		figure out text messaging scheme/frequency +0.0.1
		custom sound options +0.0.1
		add campus setting +0.0.1
		
	Done:
		put dropdown box for semester - done
		fix headless mode setting - done 
		fix twilio api support +0.0.1 - done
'''

global CRN, Term, Headless, sentText
CRN = 0
Term = ''
Headless = True
sentText = 0

class MyStatusBar(wx.StatusBar):
	
	def __init__(self, parent):
		super(MyStatusBar, self).__init__(parent)

		self.SetFieldsCount(2)
		self.SetStatusText('What class are you looking for?', 0)
		self.SetStatusText('', 1)
		self.SetStatusWidths([-1, 50])
		
		#self.icon = wx.StaticBitmap(self, bitmap=wx.Bitmap('disconnected.png'))
		self.Bind(wx.EVT_SIZE, self.OnSize)
		#self.PlaceIcon()

	def PlaceIcon(self):
		
		rect = self.GetFieldRect(1)
		#self.icon.SetPosition((rect.x+5, rect.y+1))

	def OnSize(self, e):
				
		e.Skip()
		self.PlaceIcon()
		
class PageOne(wx.Panel):
		
	def __init__(self, parent):
				
		#Initialize panel
		panel = wx.Panel.__init__(self, parent)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		#GridSizer(rows, cols, vgap, hgap)
		fgs = wx.GridSizer(4, 2, 15, 15)
	
		#Textboxes
		CRN = wx.StaticText(self, label="Class CRN")
		Term = wx.StaticText(self, label="Select Term")
		Campus = wx.StaticText(self, label="Select Campus")
		button1 = wx.StaticText(self, label="")
		button2 = wx.Button(self, label="Lookup Class")
		
		#Box types
		self.tc1 = wx.TextCtrl(self, value="#####")
		self.tc2 = wx.ComboBox(self, value="Spring", choices=["Fall" , "Spring", "Summer"], style=wx.CB_READONLY) 
		self.tc3 = wx.ComboBox(self, value="Tampa", choices=["Tampa" , "Sarasota-Manatee", "St. Petersburg", "Off Campus"], style=wx.CB_READONLY) 
		
		#Populate the grid we created
		fgs.AddMany([(CRN), (self.tc1, 1, wx.EXPAND), (Term), 
			(self.tc2, 1, wx.EXPAND), (Campus),(self.tc3, 1, wx.EXPAND),
			(button1, 1), (button2, 1, wx.EXPAND)])

		#Class search Bind
		self.Bind(wx.EVT_BUTTON, self.start_thread)

		#Box params
		hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
		self.SetSizer(hbox)
	
	
	def onClick(self, e):
		#What happens when you click the text box
		global CRN
		CRN = self.tc1.GetValue()
		global Term
		Term = self.tc2.GetStringSelection()
		self.Disable()
		Class_Notify_GUI.statusUpdate('Looking up class...', 0)		
		Start_lookup = schedule_check()
		self.Enable()
		
	
	def start_thread(self, e):
		'''Processes search in background thread'''
		import threading
		th = threading.Thread(target=self.onClick, args=(e,))
		th.start()

class PageTwo(wx.Panel):
	def __init__(self, parent):
				
		#Initialize panel
		panel = wx.Panel.__init__(self, parent)
		hbox = wx.BoxSizer(wx.HORIZONTAL)

		#GridSizer(rows, cols, vgap, hgap)
		fgs = wx.GridSizer(6, 2, 1, 0)
	
		#Textboxes
		acount_sid = wx.StaticText(self, label="Account SID")
		apiKey = wx.StaticText(self, label="Twilio Account API Key")
		api_secret = wx.StaticText(self, label="Phone Number API Secret")
		twilio_number = wx.StaticText(self, label="From number")
		your_number = wx.StaticText(self, label="To number")
		button1 = wx.StaticText(self, label="")
		button2 = wx.Button(self, label="Set key")
		
		#Box types
		self.tc1 = wx.TextCtrl(self)
		self.tc2 = wx.TextCtrl(self)
		self.tc3 = wx.TextCtrl(self)
		self.tc4 = wx.TextCtrl(self, value="+1")
		self.tc5 = wx.TextCtrl(self, value="+1") 		
		
		#Populate
		fgs.AddMany([(acount_sid), (self.tc1, 1, wx.EXPAND), 
		(apiKey), (self.tc2, 1, wx.EXPAND),
		(api_secret), (self.tc3, 1, wx.EXPAND),
		(twilio_number), (self.tc4, 1, wx.EXPAND), 
		(your_number), (self.tc5, 1, wx.EXPAND),
		(button1, 1), (button2, 1, wx.EXPAND)])

		#Class search Bind
		self.Bind(wx.EVT_BUTTON, self.onClick)

		#Box params
		hbox.Add(fgs, proportion=1, flag=wx.ALL|wx.EXPAND, border=15)
		self.SetSizer(hbox)
		
	def onClick(self, e):
		#What happens when you click the text box
		Class_Notify_GUI.statusUpdate("Number saved, I'll text you too", 0)
		global twilioSID
		global twilioapiKey
		global twilioapiSecret
		global twiliofromNumber
		global selfPhoneNumber
		twilioSID = self.tc1.GetValue()
		twilioapiKey = self.tc2.GetValue()
		twilioapiSecret = self.tc3.GetValue()
		twiliofromNumber = self.tc4.GetValue()
		selfPhoneNumber = self.tc5.GetValue()
		#Text setting will go here 
		
class PageThree(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		wx.StaticText(self, -1, "Bitcoin Donations", (10, 10))
		text = wx.adv.HyperlinkCtrl(self, -1, label="1KpJW1C9CXM3xphSv5QDHrK2XUiJBbtLh8", url="https://blockchain.info/address/1KpJW1C9CXM3xphSv5QDHrK2XUiJBbtLh8", pos=(10, 30), style=wx.adv.HL_CONTEXTMENU)
class PageFour(wx.Panel):
	def __init__(self, parent):
		wx.Panel.__init__(self, parent)
		wx.StaticText(self, -1, "Coming Soon - Default set for now", (10, 10))
		
		

class Class_Notify_GUI(wx.Frame):
  
	def __init__(self, parent, title):
		super(Class_Notify_GUI, self).__init__(parent, title=title, 
			size=(350, 275))
		self.InitUI()
		self.Centre()
		self.Show()		
		
		favicon = wx.Icon('images\icon.ico', wx.BITMAP_TYPE_ICO)
		wx.Frame.SetIcon(self, favicon)
		
	def InitUI(self):
	
		# Here we create a panel and a notebook on the panel
		p = wx.Panel(self)
		self.nb = wx.Notebook(p, wx.ID_ANY)

		# create the page windows as children of the notebook
		page1 = PageOne(self.nb)
		page2 = PageTwo(self.nb)
		page3 = PageThree(self.nb)
		page4 = PageFour(self.nb)
		#Page colors
		page1.SetBackgroundColour(wx.NullColour)
	
		# add the pages to the notebook with the label to show on the tab
		self.nb.AddPage(page1, "Main")
		self.nb.AddPage(page2, "Text Support")
		self.nb.AddPage(page3, "Buy me a coffee")
		self.nb.AddPage(page4, "Notification Tone")
		#self.Bind(wx.EVT_CLOSE, self.OnClose)
		
		sizer = wx.BoxSizer()
		sizer.Add(self.nb, 1, wx.EXPAND)
		p.SetSizer(sizer)

		#Menu Bar
		menubar = wx.MenuBar()
		
		#Initialize menu items
		fileMenu = wx.Menu()
		optionsMenu = wx.Menu()
		aboutMenu = wx.Menu()
		#File menu items
		fitem = fileMenu.Append(wx.ID_EXIT, 'Quit', 'Quit application')
		menubar.Append(fileMenu, '&File')
		#Options menu items		
		self.oitem = optionsMenu.Append(wx.ID_ANY, 'Headless Mode','Uncheck to see backend', kind=wx.ITEM_CHECK)#We add self to items that we want to call inside of other functions
		menubar.Append(optionsMenu, '&Options')
		self.checkHeadlessMode = optionsMenu.Check(self.oitem.GetId(), True)
		#About menu items
		aitem = aboutMenu.Append(wx.ID_ANY, 'About me', 'About me')
		menubar.Append(aboutMenu, '&About')
		#File Menu binds
		self.Bind(wx.EVT_MENU, self.OnQuit, fitem)
		#Option Menu binds
		self.Bind(wx.EVT_MENU, self.headlessMode, self.oitem)
		#About Menu Binds
		self.Bind(wx.EVT_MENU, self.OnAbout, aitem)
		#set menu bar
		self.SetMenuBar(menubar)
		
		#Initialize Status bar and Set
		Class_Notify_GUI.sb = MyStatusBar(self)
		self.SetStatusBar(Class_Notify_GUI.sb)
		
	def statusUpdate(message, statusboxnumber):
		'''Set status bar message initialized on main window'''
		Class_Notify_GUI.sb.SetStatusText(message, statusboxnumber)
		
	def OnQuit(self, e):
		self.Close()
		
	def headlessMode(self, e):
		global Headless
		if self.oitem.IsChecked() == True:
			Headless = True
		else:
			Headless = False
	
	def OnAbout(self, event):

		aboutInfo = wx.adv.AboutDialogInfo()
		aboutInfo.SetName("Class Notifier")
		aboutInfo.SetVersion(MY_APP_VERSION_STRING)
		aboutInfo.SetDescription(("Automatically Notify yourself when a class is available!"))
		aboutInfo.SetWebSite("https://github.com/kevin2107")
		aboutInfo.Licence = u"GNU GPL 3"

		wx.adv.AboutBox(aboutInfo)

class schedule_check():

	def __init__(self):
		#Headless Mode
		
		
		global Headless
		if Headless == 1:
			options = webdriver.ChromeOptions()
			options.add_argument('headless')
			options.add_argument('--log-level=3')
			try:
				driver = webdriver.Chrome(chrome_options=options)
			except:
				pass
		elif Headless == 0:
			options = webdriver.ChromeOptions()
			options.add_argument('--log-level=3')
			try:
				driver = webdriver.Chrome(chrome_options=options)
			except:
				pass
		try:
			driver.get("http://www.registrar.usf.edu/ssearch/search.php")
		except:
			Class_Notify_GUI.SetStatusText('Failed to load website', 0)
			pass
		#Term
		Find_Term = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[2]/td[2]/select[1]")
		Find_Term.send_keys('', Term)# Xpath --->> //*[@id="frmSearch"]/table/tbody/tr[2]/td[2]/select
		
		#Find Campus
		Find_Campus = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[4]/td[2]/select[1]")
		Find_Campus.send_keys('t')
		
		#Input CRN
		Input_CRN = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[11]/td[2]/div[1]/input[1]")
		Input_CRN.send_keys('', CRN)	
		
		#Set Sections to search
		Find_Section = driver.find_element_by_xpath("/html/body/form/table/tbody/tr[15]/td[2]/select[1]")
		Find_Section.send_keys('a')# Selects all sections because full class won't showup otherwise
		
		#Hit Search
		Hit_Search = driver.find_element_by_name("search")	 
		Hit_Search.click()
		
		#Get Open Seats & Convert string to int
		Seat_info = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[11]')
		Seats = int(Seat_info.text)
		
		#Get Subject title
		Get_Subject = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[5]')
		Subject = Get_Subject.text
		
		#Get Subject abbrev
		Get_Title = driver.find_element_by_xpath('/html/body/table/tbody/tr[2]/td[7]')
		Title = Get_Title.text

		try:
			self.send_text(twilioSID, twilioapiKey, twilioapiSecret, twiliofromNumber, selfPhoneNumber, Title)
		except:
			Class_Notify_GUI.statusUpdate("Error while sending text, check settings",0)
			pass
			
		##Notify
		self.Play_notify(Seats)
		
		try:
			# we have to wait for the page to refresh, the last thing that seems to be updated is the title
			WebDriverWait(driver, 10).until(EC.title_contains("USF - OASIS Schedule of Classes"))
			Class_Notify_GUI.statusUpdate(Subject + ': ' + Title, 0)
			Class_Notify_GUI.statusUpdate('Seats: ' + Seat_info.text, 1)
			print ('Refreshing in 15 Seconds...Press CTRL+C to end')
			print ('-----------')
		finally:
			driver.quit()	
			sleep(15)
			repeat = schedule_check()


	def send_text(self, twilioSID, twilioapiKey, twilioapiSecret, twiliofromNumber, selfPhoneNumber, title, seats):
		if seats == 0:
			Class_Notify_GUI.statusUpdate("Class Full, text not sent", 0)
		if seats > 0:
		# Your Account Sid and Auth Token from twilio.com/user/account
			account_sid = twilioSID
			api_key = twilioapiKey
			api_secret = twilioapiSecret
		# the following line needs your Twilio Account SID and Auth Token
			client = Client(api_key, api_secret, account_sid)
			message = client.messages.create(selfPhoneNumber, 
										from_=twiliofromNumber,  # twilio number
										body= title + ' is avaiable, register now with CRN: ' + CRN)
			sentText = 1					
		# change the "from_" number to your Twilio number and the "to" number
		# to the phone number you signed up for Twilio with, or upgrade your
		# account to send SMS to any phone number					

	def Play_notify(self, seats):
		if seats == 0:
			notify.init()
			notify.music.load("sounds/beep-06.wav")
			notify.music.set_volume(.01)
			notify.music.play()
		if seats > 0:
			notify.init()
			notify.music.load("sounds/whistle.mp3")
			notify.music.set_volume(.4)
			notify.music.play()	

		
if __name__ == '__main__':
  
	app = wx.App()
	MY_APP_VERSION_STRING = Current
	Class_Notify_GUI(None, title='Class notifier')
	app.MainLoop()

