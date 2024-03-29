from odoo import fields, models, api
from datetime import datetime, timedelta
# from googletrans import Translator
# import convert_numbers
from  uuid import uuid4

# translator = Translator(service_urls=['translate.googleapis.com'])
import werkzeug.urls

try:
    import qrcode
except ImportError:
    qrcode = None


class AccountMove(models.Model):
    _inherit = 'account.move'



    def testing(self):
        leng = len(self.company_id.name)
        company_name = self.company_id.name
        if 42 > leng:
            for r in range(42-leng):
                if len(company_name) != 42:
                   company_name +=' '
                else:
                    break
        else:
            if 42 < leng:
                company_name = company_name[:42]
        vat_leng = len(self.company_id.vat)
        vat_name = self.company_id.vat
        if 17 > vat_leng:
            for r in range(15 - vat_leng):
                if len(vat_name) != 15:
                    vat_name += ' '
                else:
                    break
        else:
            if 17 < leng:
                vat_name = vat_name[:17]

        amount_total = str(self.amount_total)
        amount_leng = len(str(self.amount_total))
        if len(amount_total) < 17:
            for r in range(17-amount_leng):
                if len(amount_total) != 17:
                   amount_total +=' '
                else:
                    break

        tax_leng = len(str(self.amount_tax))
        amount_tax_total = str(self.amount_tax)
        if len(amount_tax_total) < 17:
            for r in range(17-tax_leng):
                if len(amount_tax_total) != 17:
                   amount_tax_total +=' '
                else:
                    break

        # data = "*"+str(company_name)+""+str(vat_name)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+"Z"+""+amount_total+""+amount_tax_total
        # import base64
        # print(data)
        # mou = base64.b64encode(bytes(data, 'utf-8'))
        # self.decoded_data =str(mou.decode())
        #
        # qr = qrcode.QRCode(
        #     version=1,
        #     error_correction=qrcode.constants.ERROR_CORRECT_L,
        #     box_size=20,
        #     border=4,
        # )
        # data_im = str(mou.decode())
        # qr.add_data(data_im)
        # qr.make(fit=True)
        # img = qr.make_image()
        #
        # import io
        # import base64
        #
        # temp = io.BytesIO()
        # img.save(temp, format="PNG")
        # qr_image = base64.b64encode(temp.getvalue())
        # self.qr_image = qr_image
        #
        # return str(mou.decode())
        #
        # Dim
        # Data
        # As
        # String = ""
        # Dim
        # TimeAndDate
        # As
        # String = XInvoiceDate & XInvoiceTime
        invoice_date_new = (self.invoice_datetime + timedelta(hours=self.company_id.hours, minutes=self.company_id.minutes)).date()
        invoice_time_new = (self.invoice_datetime + timedelta(hours=self.company_id.hours, minutes=self.company_id.minutes)).time()
        TimeAndDate = str(invoice_date_new) + "T" + str(invoice_time_new) + "Z"
        time_length = len(str(invoice_date_new) + "T" + str(invoice_time_new) + "Z")

        # Data = (ChrW(1)).ToString() & (ChrW((company_name.Length))).ToString() & company_name
        Data = str(chr(1)) + str(chr(leng)) + self.company_id.name
        # Data += (ChrW(2)).ToString() & (ChrW((vat_name.Length))).ToString() & vat_name
        Data += (str(chr(2))) + (str(chr(vat_leng))) + vat_name
        Data += (str(chr(3))) + (str(chr(time_length))) + TimeAndDate
        # amount_total = self.amount_total
        net_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        if self.invoice_line_ids.mapped('tax_ids'):
           taxed_amount = net_amount * 0.15
        else:
            taxed_amount = float(0.00)
        amount_total = net_amount+taxed_amount

        if self.exchg_rate:
            # Data += (str(chr(4))) + (str(chr(len(str(self.amount_total*float(self.exchg_rate)))))) + str(self.amount_total*float(self.exchg_rate))
            Data += (str(chr(4))) + (str(chr(len(str(amount_total*float(self.exchg_rate)))))) + str(amount_total*float(self.exchg_rate))
            Data += (str(chr(5))) + (str(chr(len(str(taxed_amount*float(self.exchg_rate)))))) + str(taxed_amount*float(self.exchg_rate))
        else:
             Data += (str(chr(4))) + (str(chr(len(str(amount_total))))) + str(amount_total)
             Data += (str(chr(5))) + (str(chr(len(str(taxed_amount))))) + str(taxed_amount)
        data = Data
        import base64
        mou = base64.b64encode(bytes(data, 'utf-8'))
        self.decoded_data = str(mou.decode())
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
        data_im = str(mou.decode())
        qr.add_data(data_im)
        qr.make(fit=True)
        img = qr.make_image()

        import io
        import base64

        temp = io.BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_image = qr_image
        return str(mou.decode())


    def testing_qr_new_update(self):
        leng = len(self.company_id.name)
        company_name = self.company_id.name
        if 42 > leng:
            for r in range(42-leng):
                if len(company_name) != 42:
                   company_name +=' '
                else:
                    break
        else:
            if 42 < leng:
                company_name = company_name[:42]
        vat_leng = len(self.company_id.vat)
        vat_name = self.company_id.vat
        if 17 > vat_leng:
            for r in range(15 - vat_leng):
                if len(vat_name) != 15:
                    vat_name += ' '
                else:
                    break
        else:
            if 17 < leng:
                vat_name = vat_name[:17]

        amount_total = str(self.amount_total)
        amount_leng = len(str(self.amount_total))
        if len(amount_total) < 17:
            for r in range(17-amount_leng):
                if len(amount_total) != 17:
                   amount_total +=' '
                else:
                    break

        tax_leng = len(str(self.amount_tax))
        amount_tax_total = str(self.amount_tax)
        if len(amount_tax_total) < 17:
            for r in range(17-tax_leng):
                if len(amount_tax_total) != 17:
                   amount_tax_total +=' '
                else:
                    break

        # data = "*"+str(company_name)+""+str(vat_name)+""+str(self.invoice_date)+"T"+str(self.datetime_field.time())+"Z"+""+amount_total+""+amount_tax_total
        # import base64
        # print(data)
        # mou = base64.b64encode(bytes(data, 'utf-8'))
        # self.decoded_data =str(mou.decode())
        #
        # qr = qrcode.QRCode(
        #     version=1,
        #     error_correction=qrcode.constants.ERROR_CORRECT_L,
        #     box_size=20,
        #     border=4,
        # )
        # data_im = str(mou.decode())
        # qr.add_data(data_im)
        # qr.make(fit=True)
        # img = qr.make_image()
        #
        # import io
        # import base64
        #
        # temp = io.BytesIO()
        # img.save(temp, format="PNG")
        # qr_image = base64.b64encode(temp.getvalue())
        # self.qr_image = qr_image
        #
        # return str(mou.decode())
        #
        # Dim
        # Data
        # As
        # String = ""
        # Dim
        # TimeAndDate
        # As
        # String = XInvoiceDate & XInvoiceTime
        invoice_date_new = (self.invoice_datetime + timedelta(hours=self.company_id.hours, minutes=self.company_id.minutes)).date()
        invoice_time_new = (self.invoice_datetime + timedelta(hours=self.company_id.hours, minutes=self.company_id.minutes)).time()
        TimeAndDate = str(invoice_date_new) + "T" + str(invoice_time_new) + "Z"
        time_length = len(str(invoice_date_new) + "T" + str(invoice_time_new) + "Z")

        # Data = (ChrW(1)).ToString() & (ChrW((company_name.Length))).ToString() & company_name
        Data = str(chr(1)) + str(chr(leng)) + self.company_id.name
        # Data += (ChrW(2)).ToString() & (ChrW((vat_name.Length))).ToString() & vat_name
        Data += (str(chr(2))) + (str(chr(vat_leng))) + vat_name
        Data += (str(chr(3))) + (str(chr(time_length))) + TimeAndDate
        # amount_total = self.amount_total
        net_amount = self.amount_untaxed - float(self.advance) - float(self.discount_value)
        if self.invoice_line_ids.mapped('tax_ids'):
           taxed_amount = net_amount * 0.15
        else:
            taxed_amount = float(0.00)
        amount_total = net_amount+taxed_amount

        if self.exchg_rate:
            # Data += (str(chr(4))) + (str(chr(len(str(self.amount_total*float(self.exchg_rate)))))) + str(self.amount_total*float(self.exchg_rate))
            Data += (str(chr(4))) + (str(chr(len(str(amount_total*float(self.exchg_rate)))))) + str(amount_total*float(self.exchg_rate))
            Data += (str(chr(5))) + (str(chr(len(str(taxed_amount*float(self.exchg_rate)))))) + str(taxed_amount*float(self.exchg_rate))
        else:
             Data += (str(chr(4))) + (str(chr(len(str(amount_total))))) + str(amount_total)
             Data += (str(chr(5))) + (str(chr(len(str(taxed_amount))))) + str(taxed_amount)
        data = Data
        import base64
        mou = base64.b64encode(bytes(data, 'utf-8'))
        self.decoded_data = str(mou.decode())
        qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=20,
                border=4,
            )
        data_im = str(mou.decode())
        qr.add_data(data_im)
        qr.make(fit=True)
        img = qr.make_image()

        import io
        import base64

        temp = io.BytesIO()
        img.save(temp, format="PNG")
        qr_image = base64.b64encode(temp.getvalue())
        self.qr_image = qr_image
        return str(mou.decode())


