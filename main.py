import wx
from database import *
from controller import *
import wx.adv
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
import datetime
from wx.lib import masked
from ObjectListView import ObjectListView, ColumnDefn
import dialogs
import timeboard as tb
from wx.lib.wordwrap import wordwrap



Base.metadata.bind = motor
DbSession = sessionmaker(bind=motor)
# A dbSession páldány minden beillesztésnél létrehoz az adatbázisban egy bejegyzést, és ágy átmáneti zónát az objektumokhoz is. Lehetővé teszi a commit-t és a rollback használatát is a programunkban
session = DbSession()


def _wxdate2pydate(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None


def _pydate2wxdate(date):
    assert isinstance(date, (datetime.datetime, datetime.date))
    tt = date.timetuple()
    dmy = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTime.FromDMY(*dmy)

def _wxtime2pytime(time):
    assert isinstance(time, wx.DateTime)
    if time.IsValid():
        hms = map(int, time.FormatISOTime().split(':'))
        return datetime.time(*hms)
    else:
        return None

def _pytime2wxtime(time):
    assert isinstance(time, (datetime.datetime, datetime.time))
    tt = date.timetuple()
    hms = (tt[2], tt[1] - 1, tt[0])
    return wx.DateTime.FromHMS(*hms)

class NewGroupPanel(wx.Panel):
    def __init__(self, parent=None):
        #scrolled.ScrolledPanel.__init__(self, parent, -1)
        #self.SetAutoLayout(1)
        #self.SetupScrolling()
        screenSize = wx.DisplaySize()
        wx.Frame.__init__(self, parent=parent, size=screenSize)
        self.label_10 = wx.StaticText(self, -1, ("Csoport neve: "), pos=(20, 20))
        self.txtName = wx.TextCtrl(self, -1, "", pos=(350, 20), size=(200, 30))

        self.label_11 = wx.StaticText(self, -1, ("Kontakt személy neve: "), pos=(20, 60))
        self.txtContactName = wx.TextCtrl(self, -1, "", pos=(350, 60), size=(200, 30))

        self.label_12 = wx.StaticText(self, -1, ("Csoport címe: "), pos=(20, 100))
        self.txtAddress = wx.TextCtrl(self, -1, "", pos=(350, 100), size=(200, 30))

        self.label_13 = wx.StaticText(self, -1, ("E-mail címe: "), pos=(20, 140))
        self.txtEmail = wx.TextCtrl(self, -1, "", pos=(350, 140), size=(200, 30))

        self.label_14 = wx.StaticText(self, -1, ("Telefonszám: "), pos=(20, 180))
        self.txtPhone = wx.TextCtrl(self, -1, "", pos=(350, 180), size=(200, 30))

        self.label_15 = wx.StaticText(self, -1, ("Érkezés dátuma és időpontja: "), pos=(20, 220))
        self.txtDate = wx.adv.DatePickerCtrl(self, style=wx.adv.DP_DEFAULT, pos=(350, 220), size=(200, 30))
        self.txtTime = wx.adv.TimePickerCtrl(self, size=(200, -1), pos=(350, 260), style=wx.adv.TP_DEFAULT)

        self.label_16 = wx.StaticText(self, -1, ("Felnőttek száma: "), pos=(20, 300))
        self.txtFullPrice = wx.SpinCtrl(self, value='0', initial=0, pos=(350, 300), size=(200, 30))

        self.label_17 = wx.StaticText(self, -1, ("Kedvezményezettek száma (Diák/Nyugdíjas): "), pos=(20, 340))
        self.txtDiscountPrice = wx.SpinCtrl(self, value='0', initial=0, pos=(350, 340), size=(200, 30))

        self.label_18 = wx.StaticText(self, -1, ("Választott szolgáltatások: "), pos=(20, 380))
        self.txtServices = wx.TextCtrl(self, -1, "", pos=(350, 380), size=(200, 30))

        self.label_20 = wx.StaticText(self, -1, ("Fizetve? "), pos=(20, 420))
        self.txtPayed = wx.CheckBox(self, -1, "", pos=(350, 420), size=(30, 30))

        self.label_19 = wx.StaticText(self, -1, ("Megjegyzés: "), pos=(20, 460))
        self.txtDescriptions = wx.TextCtrl(self, -1, "", pos=(350, 460), size=(200, 30))

        self.okBtn = wx.Button(parent=self, label="Hozzáadás", pos=(600, 100), size=(100, 30))
        self.okBtn.Bind(event=wx.EVT_BUTTON, handler=self.AddGroup)
        self.exitBtn = wx.Button(parent=self, label="Mégse", pos=(600, 160), size=(100, 30))
        self.exitBtn.Bind(event=wx.EVT_BUTTON, handler=self.onCancel)

        self.txtName.SetFocus()

    def AddGroup(self, event):

        self.name = self.txtName.GetValue()
        self.contact_name = self.txtContactName.GetValue()
        self.address = self.txtAddress.GetValue()
        self.email = self.txtEmail.GetValue()
        self.phone = self.txtPhone.GetValue()
        self.GivenDate = _wxdate2pydate(self.txtDate.GetValue())
        self.GivenTime = _wxtime2pytime(self.txtTime.GetValue())
        self.full_price_members = self.txtFullPrice.GetValue()
        self.discount_price_members = self.txtDiscountPrice.GetValue()
        self.service = self.txtServices.GetValue()
        if self.txtPayed.GetValue():
            self.payed = True
        else:
            self.payed = False
        self.descriptions = self.txtDescriptions.GetValue()
        data = {'name': self.name, 'contact_name': self.contact_name, 'address': self.address,
                "email": self.email, 'phone': self.phone, 'date': self.GivenDate, 'time': self.GivenTime,
                'full_price': self.full_price_members, 'discount_price': self.discount_price_members,
                'service': self.service, 'payed': self.payed, "description": self.descriptions}
        group = Groups(**data)
        session.add(group)
        session.commit()
        dialogs.show_message("Sikeres rögzítés!","Siker", wx.ICON_INFORMATION)

        self.txtName.Clear()
        self.txtContactName.Clear()
        self.txtAddress.Clear()
        self.txtEmail.Clear()
        self.txtPhone.Clear()
        self.txtDate = datetime.date.today()
        self.txtTime = datetime.datetime.utcnow()
        self.txtFullPrice = self.txtFullPrice.SetValue(0)
        self.txtDiscountPrice = self.txtDiscountPrice.SetValue(0)
        self.txtServices.Clear()
        self.txtPayed = False
        self.txtDescriptions.Clear()

    def onCancel(self, event):
        self.txtName.Clear()
        self.txtContactName.Clear()
        self.txtAddress.Clear()
        self.txtEmail.Clear()
        self.txtPhone.Clear()
        self.txtDate = datetime.date.today()
        self.txtTime = datetime.datetime.utcnow()
        self.txtFullPrice = self.txtFullPrice.SetValue(0)
        self.txtDiscountPrice = self.txtDiscountPrice.SetValue(0)
        self.txtServices.Clear()
        self.txtDescriptions.Clear()
        self.txtPayed = False
        self.Close()



class EditGroupPanel(wx.Panel):
    def __init__(self, parent=None):
        #scrolled.ScrolledPanel.__init__(self, parent, -1)
        #self.SetAutoLayout(1)
        #self.SetupScrolling()
        screenSize=wx.DisplaySize()
        wx.Panel.__init__(self, parent=parent, size=screenSize)
        if not os.path.exists("csoportok.db"):
            setup_database()
        self.session = connect_to_database()
        try:
            self.group_results = get_all_records(self.session)
        except:
            self.group_results = []
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        search_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)
        # create the search related widgets
        categories = ["Csoport", "Dátum", "Szolgáltatás", "Fizetve"]
        search_label = wx.StaticText(self, label="Keresés: ")
        search_label.SetFont(font)
        search_sizer.Add(search_label, 0, wx.ALL, 5)

        self.categories = wx.ComboBox(self, value="Csoport", choices=categories)
        search_sizer.Add(self.categories, 0, wx.ALL, 5)

        self.search_ctrl = wx.SearchCtrl(self, style=wx.TE_PROCESS_ENTER)
        self.search_ctrl.Bind(wx.EVT_TEXT_ENTER, self.search)
        search_sizer.Add(self.search_ctrl, 0, wx.ALL, 5)

        self.group_results_olv = ObjectListView(self, style=wx.LC_REPORT | wx.SUNKEN_BORDER)
        self.group_results_olv.SetEmptyListMsg("Nincs ilyen bejegyzés")
        self.update_group_results()

        edit_record_btn = wx.Button(self, label="Szerkesztés")
        edit_record_btn.Bind(wx.EVT_BUTTON, self.edit_record)
        btn_sizer.Add(edit_record_btn, 0, wx.ALL, 5)

        delete_record_btn = wx.Button(self, label="Törlés")
        delete_record_btn.Bind(wx.EVT_BUTTON, self.delete_record)
        btn_sizer.Add(delete_record_btn, 0, wx.ALL, 5)

        show_all_btn = wx.Button(self, label="Mutasd mindet")
        show_all_btn.Bind(wx.EVT_BUTTON, self.on_show_all)
        btn_sizer.Add(show_all_btn, 0, wx.ALL, 5)

        #close_btn = wx.Button(self, label="Bezárás")
        #close_btn.Bind(wx.EVT_CLOSE, MainFrame.onClose)
        #btn_sizer.Add(close_btn, 0, wx.ALL, 5)

        main_sizer.Add(search_sizer)
        main_sizer.Add(self.group_results_olv, 1, wx.ALL | wx.EXPAND, 5)
        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizer(main_sizer)

    def edit_record(self, event):
        """
        Edit a record
        """
        selected_row = self.group_results_olv.GetSelectedObject()
        if selected_row is None:
            dialogs.show_message('Nincs kijelölve sor!', 'Hiba')
            return

        with dialogs.RecordDialog(self.session, selected_row, title='Módosítás', addRecord=False) as dlg:
            dlg.ShowModal()

        self.show_all_records()

    def delete_record(self, event):
        """
        Delete a record
        """
        selected_row = self.group_results_olv.GetSelectedObject()
        if selected_row is None:
            dialogs.show_message('Nincs kijelölve sor!', 'Hiba')
            return
        delete_record(self.session, selected_row.id)
        self.show_all_records()

    def show_all_records(self):
        """
        Updates the record list to show all of them
        """
        self.group_results = get_all_records(self.session)
        self.update_group_results()

    def search(self, event):
        """
        Searches database based on the user's filter
        choice and keyword
        """
        filter_choice = self.categories.GetValue()
        keyword = self.search_ctrl.GetValue()
        self.group_results = search_records(
            self.session, filter_choice, keyword)
        self.update_group_results()

    def on_show_all(self, event):
        """
        Updates the record list to show all the records
        """
        self.show_all_records()

    def update_group_results(self):
        """
        Updates the ObjectListView's contents
        """
        self.group_results_olv.SetColumns([
            ColumnDefn("Csoport", "left", 150, "name"),
            ColumnDefn("Kontakt személy", "left", 150, "contact_name"),
            ColumnDefn("Csoport címe", "left", 150, "address"),
            ColumnDefn("Email cím", "left", 150, "email"),
            ColumnDefn("Telefonszám", "left", 150, "phone"),
            ColumnDefn("Szolgáltatás", "left", 150, "service"),
            ColumnDefn("Felnőttek száma", "left", 150, "full_price"),
            ColumnDefn("Kedvezményezettek száma", "left", 150, "discount_price"),
            ColumnDefn("Dátum", "left", 150, "date"),
            ColumnDefn("Időpont","left", 150, "time"),
            ColumnDefn("Fizetve", "left", 150, "payed"),
            ColumnDefn("Megjegyzés", "left", 150, "description")
        ])
        self.group_results_olv.SetObjects(self.group_results)

    def onClose(self):
        self.Close()


class MainFrame(wx.Frame):

    def __init__(self, title):
        #scrolled.ScrolledPanel.__init__(self, parent, title)
        #self.SetAutoLayout(1)
        #self.SetupScrolling()
        screenSize=wx.DisplaySize()
        screenWidth=screenSize[1]
        screenHeight=screenSize[1]
        #super(MainFrame, self).__init__(parent=parent, title=title, size=screenSize)
        wx.Frame.__init__(self, None, wx.ID_ANY, title=title, size=screenSize)
        self.nGPanel = NewGroupPanel(self)
        self.eGPanel = EditGroupPanel(self)
        self.eGPanel.Hide()
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.nGPanel, 1, wx.EXPAND)
        self.sizer.Add(self.eGPanel, 1, wx.EXPAND)
        self.SetSizer(self.sizer)
        #self.Show()
        self.Centre()
        self.Create_MenuBar()

    def Create_MenuBar(self):
        # Creating the menubar and the menus
        self.menuBar = wx.MenuBar()
        self.GroupMenu = wx.Menu()
        self.DataBaseMenu = wx.Menu()
        self.HelpMenu = wx.Menu()

        # Adding items to Group Menu
        newGroupItem = self.GroupMenu.Append(wx.ID_NEW, "&Új csoport\tCtrl+N")
        self.Bind(wx.EVT_MENU, self.SwitchPanels, id=newGroupItem.GetId())

        editGroupItem = self.GroupMenu.Append(wx.ID_EDIT, "&Csoportok módosítása\tCtrl+E")
        self.Bind(wx.EVT_MENU, self.SwitchPanels, id=editGroupItem.GetId())

        quitItem = self.GroupMenu.Append(wx.ID_EXIT, "&Kilépés\tCtrl+W")
        self.Bind(wx.EVT_MENU, self.onClose, id=quitItem.GetId())

        aboutItem = self.HelpMenu.Append(wx.ID_ABOUT, "&Névjegy")
        self.Bind(wx.EVT_MENU, self.onAbout, aboutItem)
        self.menuBar.Append(self.GroupMenu, "&Csoportok")
        self.menuBar.Append(self.DataBaseMenu, "&Foglalások")
        self.menuBar.Append(self.HelpMenu, "&Súgó")
        self.SetMenuBar(self.menuBar)

        # Create status bar
        self.status_bar = self.CreateStatusBar(1)

        msg = 'Hare Krisna! (c) Raghava Dasa - 2020'
        self.status_bar.SetStatusText(msg)

    def onAbout(self, event):
        info = wx.adv.AboutDialogInfo()
        info.SetIcon(wx.Icon('app_icon.jpeg', wx.BITMAP_TYPE_JPEG))
        info.Name = "Bejelentkezett csoportok"
        info.Version = "1.0"
        info.Copyright = "(C) 2020 Krisna-völgy, Raghava Dasa <raghava@krisna.hu>"
        info.Description = ("Csoportfoglalást rendszerező alkalmazás ")
        info.WebSite = ("https://www.krisnavolgy.hu", "Krisna-völgy")
        info.Developers = ["Raghava Dasa"]
        info.License = ("Teljesen ingyenes és nyílt forráskódú!")
        wx.adv.AboutBox(info)

    def newGroup(self,event):

        self.nGPanel=NewGroupPanel(self)
        if self.eGPanel.IsShown():
            self.SetTitle("Új csoport regisztrációja")
            self.eGPanel.Hide()
            self.nGPanel.Show()



    def editGroup(self, event):
        self.eGPanel = EditGroupPanel(self)
        if self.nGPanel.IsShown():
            self.SetTitle("Csoport foglalások szerkesztése")
            self.nGPanel.Hide()
            self.eGPanel.Show()

    def onClose(self, event):
        self.Close()

    def SwitchPanels(self, event):
        if self.nGPanel.IsShown():
            self.SetTitle("Csoport foglalások szerkesztése")
            self.nGPanel.Hide()
            self.eGPanel.Show()
        else:
            self.SetTitle("Új csoport regisztrációja")
            self.eGPanel.Hide()
            self.nGPanel.Show()

        self.Layout()

    def on_new_group(self, event):
        title="Új csoport regisztrációja"
        self.newGroup = NewGroupPanel(title=title, parent=self.GetParent())
        #self.frame_number += 1

    def on_edit_group(self,event):
        title = "Csoportok módosítása"
        self.editGroup = EditGroupPanel(title=title, parent=self.GetParent())

    def ListBookings(self):
        pass


#class MainApp(wx.App):
 #   def __init__(self):
  #      super().__init__(clearSigInt=True)
  #      self.InitFrame()

   # def InitFrame(self):
   #     frame = MainFrame(parent=None, title="Csoport bejelentkezések")
   #     frame.Show()


if __name__ == '__main__':
    #app = MainApp()
    app = wx.App(False)
    frame = MainFrame(title="Csoport bejelentkezések")
    frame.Show()
    frame.Centre()
    app.MainLoop()
