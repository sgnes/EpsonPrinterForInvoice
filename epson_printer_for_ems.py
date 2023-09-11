from escpos.printer import Usb
import re
from datetime import date
class EpsonPrinter(object):
    SenderName = "SenderName"
    SenderPhone = "SenderPhone"
    SenderAddr = "SenderAddr"
    ReceiverName = "ReceiverName"
    ReceiverPhone = "ReceiverPhone"
    ReceiverAddr = "ReceiverAddr"

    def __init__(self, data, usbidVendor=0x04b8, idProduct=0x0006a, usb_args=0) -> None:
        self.p = Usb(usbidVendor, idProduct, usb_args)
        self.info = data
    
    def checkInvoiceInformationIntegrity(self):
        l = [self.SenderAddr, self.SenderName, self.SenderPhone,self.ReceiverAddr, self.ReceiverName, self.ReceiverPhone]
        for i in l:
            if i not in self.info:
                return False
        return True

    def printInvoiceForsinglePaper(self):
        try:
            t = date.today()

            sender_name = self.info[self.SenderName]
            sender_phone = self.info[self.SenderPhone]
            sender_addr =  self.info[self.SenderAddr]
            sender_addr_list = re. findall(r'.{22}', sender_addr)

            receiver_name = self.info[self.ReceiverName]
            receiver_phone = self.info[self.ReceiverPhone]
            receiver_addr = self.info[self.ReceiverAddr]
            receiver_addr_list = re.findall(r'.{22}', receiver_addr)

            self.p.text("\n")
            self.p.text("\n")
            self.p.text("\n")
            self.p.text("\n")
            self.p._raw("     {}                 {}\n".format(sender_name, sender_phone).encode("GB18030"))
            self.p.text("\n")
            self.p.text("\n")
            for i in sender_addr_list:
                self.p._raw("     {}\n".format(i).encode("GB18030"))
            for i in range(0,4-len(sender_addr_list),1):
                self.p.text("\n")

            self.p.text("\n")
            self.p._raw("     {}         {}   {}  {}    {}\n".format(receiver_name.ljust(10),
                                                            receiver_phone.ljust(45),
                                                            t.year,
                                                            t.month,
                                                            t.day).encode("GB18030"))
            self.p.text("\n")
            self.p.text("\n")
            for i in receiver_addr_list:
                self.p._raw("     {}\n".format(i).encode("GB18030"))
            for i in range(0,4-len(receiver_addr_list),1):
                self.p.text("\n")
                {"Print successfully!"}, 200
        except Exception as e:
            self.print(e)
            return {e}, 500
        
    





