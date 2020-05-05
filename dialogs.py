# dialogs.py

import controller
import wx
import wx.adv
import datetime


def _wxdate2pydate(date):
    assert isinstance(date, wx.DateTime)
    if date.IsValid():
        ymd = map(int, date.FormatISODate().split('-'))
        return datetime.date(*ymd)
    else:
        return None

def _wxtime2pytime(time):
    assert isinstance(time, wx.DateTime)
    if time.IsValid():
        hms = map(int, time.FormatISOTime().split(':'))
        return datetime.time(*hms)
    else:
        return None

class RecordDialog(wx.Dialog):
    """
    Add / Modify Record dialog
    """

    def __init__(self, session, row=None, title="Add", addRecord=True):
        """Constructor"""
        super().__init__(None, title="%s Record" % title)
        self.addRecord = addRecord
        self.selected_row = row
        self.session = session
        if row:
            group_name = self.selected_row.name
            group_contact_name = self.selected_row.contact_name
            group_address = self.selected_row.address
            group_email = self.selected_row.email
            group_phone = self.selected_row.phone
            group_date = self.selected_row.date
            group_time = self.selected_row.time
            group_payed = self.selected_row.payed
            group_created = self.selected_row.created
            group_modified = self.selected_row.modified
            group_service = self.selected_row.service
            group_full_price = self.selected_row.full_price
            group_discount_price = self.selected_row.discount_price
            group_description = self.selected_row.description
        else:
            group_name = group_contact_name = group_address = group_email = group_phone = group_service = group_description = ""
            group_payed = False
            group_full_price = group_discount_price = 0
            group_date = group_modified = group_created = datetime.date.today()
            group_time= datetime.datetime.utcnow()

        # create the sizers
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        group_sizer = wx.BoxSizer(wx.HORIZONTAL)
        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # create some widgets
        size = (300, -1)
        font = wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD)

        name_lbl = wx.StaticText(self, label="Csoport neve:", size=size)
        name_lbl.SetFont(font)
        self.name_txt = wx.TextCtrl(self, value=group_name)
        main_sizer.Add(self.row_builder([name_lbl, self.name_txt]),
                       0, wx.ALL)

        cname_lbl = wx.StaticText(self, label="Kontakt személy:", size=size)
        cname_lbl.SetFont(font)
        self.cname_txt = wx.TextCtrl(self, value=group_contact_name)
        main_sizer.Add(self.row_builder([cname_lbl, self.cname_txt]),
                       0, wx.ALL)

        address_lbl = wx.StaticText(self, label="Cím:", size=size)
        address_lbl.SetFont(font)
        self.address_txt = wx.TextCtrl(self, value=group_address)
        main_sizer.Add(self.row_builder([address_lbl, self.address_txt]),
                       0, wx.ALL)

        email_lbl = wx.StaticText(self, label="E-mail cím:", size=size)
        email_lbl.SetFont(font)
        self.email_txt = wx.TextCtrl(self, value=group_email)
        main_sizer.Add(self.row_builder([email_lbl, self.email_txt]),
                       0, wx.ALL)

        phone_lbl = wx.StaticText(self, label="Telefonszám:", size=size)
        phone_lbl.SetFont(font)
        self.phone_txt = wx.TextCtrl(self, value=group_phone)
        main_sizer.Add(self.row_builder([phone_lbl, self.phone_txt]),
                       0, wx.ALL)

        vdate_lbl = wx.StaticText(self, label="Érkezés dátuma és időpontja:", size=size)
        vdate_lbl.SetFont(font)
        self.vdate_txt = wx.TextCtrl(self, value= datetime.datetime.strftime(group_date,"%Y-%m-%d"))
        main_sizer.Add(self.row_builder([vdate_lbl, self.vdate_txt]),
                       0, wx.ALL)
        self.vtime_txt = wx.TextCtrl(self, value=datetime.datetime.strftime(group_time,"%H:%M"))
        main_sizer.Add(self.row_builder([vdate_lbl, self.vtime_txt]),
                       0, wx.ALL)




        ok_btn = wx.Button(self, label="%s Book" % title)
        ok_btn.Bind(wx.EVT_BUTTON, self.on_record)
        btn_sizer.Add(ok_btn, 0, wx.ALL, 5)
        cancel_btn = wx.Button(self, label="Close")
        cancel_btn.Bind(wx.EVT_BUTTON, self.on_close)
        btn_sizer.Add(cancel_btn, 0, wx.ALL, 5)

        main_sizer.Add(btn_sizer, 0, wx.CENTER)
        self.SetSizerAndFit(main_sizer)

    def on_close(self, event):
        """
        Close the dialog
        """
        self.Close()

    def get_data(self):
        group_dict = {}

        Name = self.name_txt.GetValue()
        cName = self.cname_txt.GetValue()
        Address = self.address_txt.GetValue()
        Email = self.email_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Date = self.vdate_txt.GetValue()
        Time = self.vtime_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()
        Phone = self.phone_txt.GetValue()

        if fName == "" or title == "":
            show_message("Author and Title are Required!",
                         "Error")
            return None, None

        if "-" in isbn:
            isbn = isbn.replace("-", "")
        author_dict["first_name"] = fName
        author_dict["last_name"] = lName
        book_dict["title"] = title
        book_dict["isbn"] = isbn
        book_dict["publisher"] = publisher

        return author_dict, book_dict

    def on_edit(self):
        """
        Edit a record in the database
        """
        group_dict = self.get_data()
        combo_dict = {**group_dict}
        controller.edit_record(self.session, self.selected_row.id, combo_dict)
        show_message("Sikeres szerkesztés!", "Siker",
                     wx.ICON_INFORMATION)
        self.Close()

    def on_record(self, event):
        """
        Add or edit a record
        """
        self.on_edit()
        #self.title_txt.SetFocus()

    def row_builder(self, widgets):
        """
        Helper function for building a row of widgets
        """
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        lbl, txt = widgets
        sizer.Add(lbl, 0, wx.ALL, 5)
        sizer.Add(txt, 1, wx.ALL, 5)
        return sizer


def show_message(message, caption, flag=wx.ICON_ERROR):
    """
    Show a message dialog
    """
    msg = wx.MessageDialog(None, message=message,caption=caption, style=flag)
    msg.ShowModal()
    msg.Destroy()


if __name__ == "__main__":
    app = wx.App(False)
    dlg = RecordDialog(session=None)
    dlg.ShowModal()
    dlg.Destroy()
    app.MainLoop()