from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.uic import loadUiType
import datetime
import sys
import peewee
import pymysql as MySQLdb
from math import ceil
from barcode import EAN13
from reportlab.platypus import SimpleDocTemplate,Table,TableStyle
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
import os
import subprocess
import platform
#from sys import platform
MainUi,_= loadUiType('main.ui')


def isfloat(x):
    try:
        float(x)
        return True
    except ValueError:
        return False
def isint(x):
    try:
        int(x)
        return True
    except ValueError:
        return False

class Main(QMainWindow, MainUi):
    def __init__(self, parent=None):##################instructor
        super (Main, self).__init__(parent)
        QMainWindow.__init__(self)
        self.db_connect()
        self.setupUi(self)
        self.handle_buttons()
        self.handle_ui()
        self.first_open()  
        
################################################
    def empty_returnsell(self):
        self.lineEdit_57.setText('')
        self.lineEdit_80.setText('')
        self.lineEdit_91.setText('')
        self.lineEdit_45.setText('')
        self.lineEdit_89.setText('')
        self.lineEdit_46.setText('')
        self.lineEdit_48.setText('')
        self.lineEdit_82.setText('')
        self.lineEdit_87.setText('')
        self.lineEdit_49.setText('')
        self.lineEdit_88.setText('')
        self.lineEdit_51.setText('0')
        self.lineEdit_50.setText('')
        self.lineEdit_53.setText('')
        self.lineEdit_90.setText('')
        self.lineEdit_105.setText('')
        self.lineEdit_57.setEnabled(True)
        self.lineEdit_88.setStyleSheet('')
        self.lineEdit_49.setStyleSheet('')

        while self.tableWidget_4.rowCount()>0:
            self.tableWidget_4.removeRow(0)
        self.cur.execute('''DELETE FROM temp_bill WHERE move=%s''',('rsell'))
        self.db.commit()
        self.show_returnsales()
################################################# empty sell screen
    def empty_sell(self):
        self.lineEdit_17.setText('')
        self.lineEdit_18.setText('')
        self.lineEdit_37.setText('')
        self.lineEdit_38.setText('')
        self.lineEdit_78.setText('')
        self.lineEdit_39.setText('')
        self.lineEdit_40.setText('')
        self.lineEdit_81.setText('')
        self.lineEdit_83.setText('')
        self.lineEdit_41.setText('')
        self.lineEdit_84.setText('')
        self.lineEdit_43.setText('0')
        self.lineEdit_42.setText('')
        self.lineEdit_44.setText('')
        self.lineEdit_79.setText('')
        self.lineEdit_104.setText('')
        self.lineEdit_17.setEnabled(True)
        self.lineEdit_84.setStyleSheet('')
        self.lineEdit_41.setStyleSheet('')
        while self.tableWidget_3.rowCount()>0:
            self.tableWidget_3.removeRow(0)
        self.cur.execute('''DELETE FROM temp_bill WHERE move=%s''',('sell'))
        self.db.commit()
        self.show_sales()
################################################empty purchase screen
    def empty_purchase(self):
        self.lineEdit_69.setText('')
        self.lineEdit_70.setText('')
        self.lineEdit_71.setText('')
        self.lineEdit_47.setText('')
        self.lineEdit_93.setText('')
        self.lineEdit_63.setText('')
        self.lineEdit_64.setText('')
        self.lineEdit_85.setText('')
        self.lineEdit_86.setText('')
        self.lineEdit_65.setText('')
        self.lineEdit_92.setText('')
        self.lineEdit_67.setText('0')
        self.lineEdit_66.setText('')
        self.lineEdit_68.setText('')
        self.lineEdit_94.setText('')
        self.lineEdit_107.setText('')
        self.lineEdit_108.setText('')
        self.lineEdit_69.setEnabled(True)
        self.lineEdit_92.setStyleSheet('')
        self.lineEdit_65.setStyleSheet('')

        while self.tableWidget_5.rowCount()>0:
            self.tableWidget_5.removeRow(0)
        self.cur.execute('''DELETE FROM temp_bill WHERE move=%s''',('pur'))
        self.db.commit()
        self.show_purchase()
#######################################################empty return purchase screen
    def empty_returnpurchase(self):
        self.lineEdit_97.setText('')
        self.lineEdit_98.setText('')
        self.lineEdit_103.setText('')
        self.lineEdit_72.setText('')
        self.lineEdit_101.setText('')
        self.lineEdit_73.setText('')
        self.lineEdit_74.setText('')
        self.lineEdit_96.setText('')
        self.lineEdit_99.setText('')
        self.lineEdit_75.setText('')
        self.lineEdit_100.setText('')
        self.lineEdit_77.setText('0')
        self.lineEdit_76.setText('')
        self.lineEdit_95.setText('')
        self.lineEdit_102.setText('')
        self.lineEdit_109.setText('')
        self.lineEdit_97.setEnabled(True)
        self.lineEdit_75.setStyleSheet('')
        self.lineEdit_109.setStyleSheet('')

        while self.tableWidget_9.rowCount()>0:
            self.tableWidget_9.removeRow(0)
        self.cur.execute('''DELETE FROM temp_bill WHERE move=%s''',('rpur'))
        self.db.commit()
        self.show_returnpur()
###########################################################

    def handle_buttons(self):##################program buttons
##################################### moving tabs buttons
        self.pushButton.clicked.connect(self.show_items)
        self.pushButton_2.clicked.connect(self.show_cl_ven)
        self.pushButton_3.clicked.connect(self.show_deb_bra)
        self.pushButton_4.clicked.connect(self.show_finance)
        self.pushButton_5.clicked.connect(self.show_employees)
        self.pushButton_67.clicked.connect(self.show_employees_absence_tab)
        self.pushButton_64.clicked.connect(self.show_sales)
        self.pushButton_65.clicked.connect(self.show_purchase)
        self.pushButton_25.clicked.connect(self.show_report)
        self.pushButton_78.clicked.connect(self.show_returnsales)
        self.pushButton_79.clicked.connect(self.show_returnpur)
        self.pushButton_91.clicked.connect(self.show_barcode_tab)
#####################################saving
        self.pushButton_14.clicked.connect(self.item_save)
        self.pushButton_30.clicked.connect(self.item_find)
        self.pushButton_21.clicked.connect(self.client_save)
        self.pushButton_22.clicked.connect(self.vendor_save)
        self.pushButton_20.clicked.connect(self.client_find)
        self.pushButton_23.clicked.connect(self.vendor_find)
        self.pushButton_38.clicked.connect(self.client_new)
        self.pushButton_42.clicked.connect(self.client_edit)
        self.pushButton_26.clicked.connect(self.vendor_edit)
        self.pushButton_29.clicked.connect(self.vendor_new)
        self.pushButton_18.clicked.connect(self.depository_save)
        self.pushButton_43.clicked.connect(self.branch_save)
        self.pushButton_8.clicked.connect(self.employee_save)
#####################################employee absence
        self.pushButton_11.clicked.connect(self.employee_leaving)
        self.pushButton_10.clicked.connect(self.employee_comming)
#####################################login
        self.pushButton_6.clicked.connect(self.login)
        self.pushButton_32.clicked.connect(self.create_first_attribute)
#####################################item moves
        self.pushButton_37.clicked.connect(self.stockedit_remove)
        self.pushButton_35.clicked.connect(self.stockedit_add)
        self.pushButton_36.clicked.connect(self.stockedit_show)
        self.pushButton_40.clicked.connect(self.stockmove_show)
        self.pushButton_41.clicked.connect(self.stockmove_move)
        self.pushButton_44.clicked.connect(self.stockmove_startover)
        self.pushButton_39.clicked.connect(self.stockedit_startover)
        self.pushButton_17.clicked.connect(self.item_new)
        self.pushButton_13.clicked.connect(self.item_edit)
#######################################finance tab
        self.pushButton_47.clicked.connect(self.safe_move_money_out)
        self.pushButton_90.clicked.connect(self.safe_move_money_in)
        self.pushButton_46.clicked.connect(self.drawer_move_money)
        self.pushButton_57.clicked.connect(self.client_show_balance)
        self.pushButton_66.clicked.connect(self.vendor_show_balance)
        self.pushButton_31.clicked.connect(self.client_take_money)
        self.pushButton_15.clicked.connect(self.client_give_money)
        self.pushButton_27.clicked.connect(self.clven_startover)
        self.pushButton_48.clicked.connect(self.vendor_take_money)
        self.pushButton_24.clicked.connect(self.vendor_give_money)
        self.comboBox_10.currentIndexChanged.connect(self.get_safe_drawer_client)
        self.comboBox_12.currentIndexChanged.connect(self.get_safe_drawer_vendor)
#############################################sales tab
        self.pushButton_55.clicked.connect(self.sell_search)
        self.pushButton_50.clicked.connect(self.sell_additem)
        self.pushButton_49.clicked.connect(self.sell_showclient)
        self.pushButton_45.clicked.connect(self.sell_remove_client)
        self.pushButton_51.clicked.connect(self.sell_sell)
        self.pushButton_63.clicked.connect(self.sell_removeitem)
        self.pushButton_54.clicked.connect(self.return_sell_showclient)
        self.pushButton_70.clicked.connect(self.return_sell_removeclient)
        self.pushButton_69.clicked.connect(self.return_sell_search)
        self.pushButton_52.clicked.connect(self.return_sell_additem)
        self.pushButton_71.clicked.connect(self.returnsell_removeitem)
        self.pushButton_53.clicked.connect(self.returnsell_return)
        self.comboBox_2.currentIndexChanged.connect(self.get_safe_drawer_returnsell)
        self.comboBox_4.currentIndexChanged.connect(self.get_safe_drawer_purchase)
        
#################################################################purchase
        self.pushButton_60.clicked.connect(self.purchase_showvendor)
        self.pushButton_61.clicked.connect(self.purchase_removevendor)
        self.pushButton_59.clicked.connect(self.purchase_search)
        self.pushButton_56.clicked.connect(self.purchase_additem)
        self.pushButton_72.clicked.connect(self.purchase_removeitem)
        self.pushButton_58.clicked.connect(self.purchase_purchase)
        self.pushButton_75.clicked.connect(self.return_purchase_showvendor)
        self.pushButton_76.clicked.connect(self.return_purchase_removevendor)
        self.pushButton_74.clicked.connect(self.return_purchase_search)
        self.pushButton_62.clicked.connect(self.return_purchase_additem)
        self.pushButton_77.clicked.connect(self.return_purchase_removeitem)
        self.pushButton_73.clicked.connect(self.return_purchase_return)
       
##############################################reports tab
        self.pushButton_80.clicked.connect(self.show_employee_reporttab)
        self.pushButton_82.clicked.connect(self.show_expenses_reporttab)
        self.pushButton_84.clicked.connect(self.show_clven_reporttab)
        self.pushButton_86.clicked.connect(self.show_itemsfast_reporttab)
        self.pushButton_81.clicked.connect(self.show_itemsmovement_reporttab)
        self.pushButton_88.clicked.connect(self.show_zeros_reporttab)
        self.pushButton_89.clicked.connect(self.show_bill_reporttab)
        self.pushButton_85.clicked.connect(self.show_orderassold_reporttab)
        self.pushButton_87.clicked.connect(self.show_profit_reporttab)
        
        
#################################################emps report tab
        self.pushButton_92.clicked.connect(self.show_employee_absence)
        self.pushButton_9.clicked.connect(self.show_employees_data)
######################################################expenses report
        self.pushButton_28.clicked.connect(self.show_expenses_report)
############################################################clients vendors report
        self.pushButton_33.clicked.connect(self.show_clients_report)
        self.pushButton_34.clicked.connect(self.show_vendors_report)
####################################################################items report
        self.pushButton_19.clicked.connect(self.show_items_fastreport)
        self.pushButton_16.clicked.connect(self.show_items_movementreport)
        self.pushButton_98.clicked.connect(self.show_zeros_report)
        self.pushButton_99.clicked.connect(self.show_bills_report)
        self.pushButton_100.clicked.connect(self.show_bill_detailreport)
        self.pushButton_101.clicked.connect(self.show_assold_report)
        self.pushButton_102.clicked.connect(self.send_topurchase)
        self.pushButton_105.clicked.connect(self.send_topurchase_showvendor)
        self.pushButton_106.clicked.connect(self.send_topurchase_removevendor)
        self.pushButton_103.clicked.connect(self.show_profit_tab)
 ########################################################################3return press
        self.lineEdit_54.returnPressed.connect(self.login)
#########################################################################
        self.pushButton_104.clicked.connect(self.show_item_forbarcode)
        self.pushButton_107.clicked.connect(self.add_item_forbarcode)
        self.pushButton_68.clicked.connect(self.print_barcode)
##############################################################################printing
        self.pushButton_93.clicked.connect(self.print_profit)
        self.pushButton_94.clicked.connect(self.print_absence)
        self.pushButton_95.clicked.connect(self.print_expenses)
        self.pushButton_96.clicked.connect(self.print_items_fast_report)
        self.pushButton_97.clicked.connect(self.print_item_movement)
        self.pushButton_108.clicked.connect(self.print_bills)
        self.pushButton_109.clicked.connect(self.print_bill_details)
        self.pushButton_110.clicked.connect(self.print_assold)

####################################login and UI functions
    def first_open(self):
        self.cur.execute('''SELECT * FROM bill_no''')
        check=self.cur.fetchall()
        if check==():
            self.cur.execute('''INSERT INTO bill_no(number) VALUES(%s)''',(100))
            self.db.commit()
            self.tabWidget.setCurrentIndex(9)
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_64.setEnabled(False)
            self.pushButton_78.setEnabled(False)
            self.pushButton_65.setEnabled(False)
            self.pushButton_79.setEnabled(False)
            self.pushButton_25.setEnabled(False)
        else:
            self.tabWidget.setCurrentIndex(6)

##################################3
    def create_first_attribute(self):
        branch=self.lineEdit_62.text()
        comment=self.textEdit_8.toPlainText()

        name=self.lineEdit_19.text()
        password=self.lineEdit_61.text()
        branch=self.lineEdit_62.text()
        dedication='MANAGER'
        adminity='ADMIN'
        date=date=datetime.date.today()
        comment1=self.textEdit_8.toPlainText()

        if branch==''or name=='' or password=='':
            QMessageBox.about(self,'caution','branch, name, password is mandatory')


        else:
            self.cur.execute('''
            INSERT INTO branch(name,comment)
            VALUES(%s,%s)
            ''',(branch,comment))
            self.db.commit()

            self.cur.execute('''
            INSERT INTO employees(name,password,branch,
            dedicate, adminity, join_date, comment)
            VALUES(%s,%s,%s,%s,%s,%s,%s)
            ''',(name,password,branch,dedication,adminity,date,comment1))
            self.db.commit()

            self.cur.execute('''
            SELECT name FROM employees
            ''')
            employees = self.cur.fetchall()
            for name in employees:
                self.comboBox_33.addItem(name[0])
            self.cur.execute('''
            SELECT name FROM branch
            ''')
            branchs = self.cur.fetchall()
            for branch in branchs:
                self.comboBox_32.addItem(branch[0])
            self.tabWidget.setCurrentIndex(6)
            self.lineEdit_19.setText('')
            self.lineEdit_61.setText('')
            self.textEdit_12.setText('')
            self.lineEdit_62.setText('')
            self.textEdit_8.setText('')
######################################
    def login(self):
        empname=self.comboBox_33.currentText()
        brname=self.comboBox_32.currentText()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        password=self.lineEdit_54.text()

        self.cur.execute('''SELECT password,auth1,auth2,auth3,auth4,auth5,auth6,auth7,auth8,auth9,auth10,auth11 
        FROM employees WHERE name=%s''',(empname))
        check=self.cur.fetchall()

        if password == str(check[0][0]):
            self.cur.execute('''
                INSERT INTO default_employee(employee, log_date, log_time)
                VALUES(%s,%s,%s)
                ''',(empname,date,time))
            self.db.commit()
            self.cur.execute('''
               INSERT INTO default_branch(branch, log_date,log_time)
               VALUES(%s,%s,%s)
               ''',(brname,date,time))
            self.db.commit()
            self.cur.execute('''SELECT adminity FROM employees WHERE name=%s''',(empname))
            adminity=self.cur.fetchall()
            if adminity[0][0] == 'ADMIN':
                self.lineEdit_54.setText('')
                self.tabWidget.setCurrentIndex(12)
                self.pushButton.setEnabled(True)#items tab
                self.pushButton_2.setEnabled(True)#clvend tab
                self.pushButton_3.setEnabled(True)#stores tab
                self.pushButton_4.setEnabled(True)#finance
                self.pushButton_5.setEnabled(True)#employee tab
                self.pushButton_64.setEnabled(True)#sales tab
                self.pushButton_78.setEnabled(True)#return sales tab
                self.pushButton_65.setEnabled(True)#purchase tab
                self.pushButton_79.setEnabled(True)#return purchase tab
                self.pushButton_25.setEnabled(True)#reports tab
                self.pushButton_67.setEnabled(True)#absence tab
                self.pushButton_91.setEnabled(True)#absence tab
            else:
                self.lineEdit_54.setText('')
                self.tabWidget.setCurrentIndex(5)
                if check[0][1]=='1':
                    self.pushButton.setEnabled(True)#items tab
                if check[0][2]=='1':
                    self.pushButton_2.setEnabled(True)#clvend tab
                if check[0][3]=='1':
                    self.pushButton_3.setEnabled(True)#stores tab
                if check[0][4]=='1':
                    self.pushButton_4.setEnabled(True)#finance
                if check[0][5]=='1':
                    self.pushButton_5.setEnabled(True)#employee tab
                if check[0][6]=='1':
                    self.pushButton_67.setEnabled(True)#absence tab
                if check[0][7]=='1':
                    self.pushButton_64.setEnabled(True)#sales tab
                if check[0][8]=='1':
                    self.pushButton_78.setEnabled(True)#return sales tab
                if check[0][9]=='1':
                    self.pushButton_65.setEnabled(True)#purchase tab
                if check[0][10]=='1':
                    self.pushButton_79.setEnabled(True)#return purchase tab
                if check[0][11]=='1':
                    self.pushButton_25.setEnabled(True)#reports tab
           
        else:
            QMessageBox.about(self,'caution','wrong password')

#####################################
    def get_safe_drawer_returnsell(self):
        if self.comboBox_2.currentText()=='SAFE':
            qin=0
            qout=0
            #############show safe balance
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin+=row[0]
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout+=row[0]
            balance=qin-qout
            self.lineEdit_106.setText(str(balance))
            ##################show drawer balance

        elif self.comboBox_2.currentText()=='DRAWER':
            qin1=0
            qout1=0
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin1+=row[0]
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout1+=row[0]
            balance=qin1-qout1
            self.lineEdit_106.setText(str(balance))
####################################
    def get_safe_drawer_purchase(self):
        if self.comboBox_4.currentText()=='SAFE':
            qin=0
            qout=0
            #############show safe balance
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin+=row[0]
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout+=row[0]
            balance=qin-qout
            self.lineEdit_107.setText(str(balance))
            ##################show drawer balance

        elif self.comboBox_4.currentText()=='DRAWER':
            qin1=0
            qout1=0
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin1+=row[0]
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout1+=row[0]
            balance=qin1-qout1
            self.lineEdit_107.setText(str(balance))
#############################################
    def get_safe_drawer_client(self):
        if self.comboBox_10.currentText()=='SAFE':
            qin=0
            qout=0
            #############show safe balance
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin+=row[0]
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout+=row[0]
            balance=qin-qout
            self.lineEdit_111.setText(str(balance))
            ##################show drawer balance

        elif self.comboBox_10.currentText()=='DRAWER':
            qin1=0
            qout1=0
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin1+=row[0]
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout1+=row[0]
            balance=qin1-qout1
            self.lineEdit_111.setText(str(balance))
            
###########################################
    def get_safe_drawer_vendor(self):
        if self.comboBox_12.currentText()=='SAFE':
            qin=0
            qout=0
            #############show safe balance
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin+=row[0]
            self.cur.execute('''
            SELECT amount FROM safe_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout+=row[0]
            balance=qin-qout
            self.lineEdit_112.setText(str(balance))
            ##################show drawer balance

        elif self.comboBox_12.currentText()=='DRAWER':
            qin1=0
            qout1=0
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('in'))
            allin =self.cur.fetchall()
            for row in allin:
                qin1+=row[0]
            self.cur.execute('''
            SELECT amount FROM drawer_moves WHERE move=%s
            ''',('out'))
            allout =self.cur.fetchall()
            for row in allout:
                qout1+=row[0]
            balance=qin1-qout1
            self.lineEdit_112.setText(str(balance))

###########################################
    def handle_ui(self):
        self.setFixedSize(1140,700)
        self.tabWidget.tabBar().setVisible(False)
        self.tabWidget_6.tabBar().setVisible(False)
        self.tabWidget_4.tabBar().setVisible(False)
        self.tabWidget_7.tabBar().setVisible(False)
        self.tabWidget_8.tabBar().setVisible(False)
        self.cur.execute('''
            SELECT name FROM branch
            ''')
        branchs = self.cur.fetchall()
        for branch in branchs:
            self.comboBox_32.addItem(branch[0])

        self.cur.execute('''
            SELECT name FROM employees
            ''')
        employees = self.cur.fetchall()
        for name in employees:
            self.comboBox_33.addItem(name[0])
        self.comboBox_33.setFocus()
############################################
    def reset_password(self):
        pass
#################################################
    def db_connect(self):
        self.db=MySQLdb.connect(host='localhost', user='root',
                                password='toor',db='sales_prog')
        self.cur=self.db.cursor()
        print('connected')
################################################

#####################################moving tabs functions
    def show_items(self):
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_16.clear()
        self.comboBox_19.clear()
        self.comboBox_20.clear()

        self.cur.execute('''
            SELECT name FROM branch
            ''')
        branchs = self.cur.fetchall()
        for branch in branchs:
            self.comboBox_16.addItem(branch[0])
            self.comboBox_19.addItem(branch[0])
            self.comboBox_20.addItem(branch[0])
        self.cur.execute('''
            SELECT name FROM depository
            ''')
        depos = self.cur.fetchall()
        for depo in depos:
            self.comboBox_16.addItem(depo[0])
            self.comboBox_19.addItem(depo[0])
            self.comboBox_20.addItem(depo[0])
         ###########################################    
        items_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_34)
        autocomplete(items_list,self.lineEdit_56)
        autocomplete(items_list,self.lineEdit)
        
######################################################
    def show_cl_ven(self):
        self.tabWidget.setCurrentIndex(1)
        # self.cur.execute('''INSERT INTO bill_no(number) VALUES(%s)''',(100))
        # self.db.commit()
###################################################
    def show_deb_bra(self):
        self.tabWidget.setCurrentIndex(2)
        self.comboBox_17.clear()

        self.cur.execute('''
            SELECT name FROM branch
            ''')
        branchs = self.cur.fetchall()
        for branch in branchs:
            self.comboBox_17.addItem(branch[0])
######################################################
    def show_finance(self):
        qin=0
        qout=0
        self.tabWidget.setCurrentIndex(3)
        #############show safe balance
        self.cur.execute('''
        SELECT amount FROM safe_moves WHERE move=%s
        ''',('in'))
        allin =self.cur.fetchall()
        #print(allin)
        for row in allin:
            qin+=row[0]
            #print(qin)
        self.cur.execute('''
        SELECT amount FROM safe_moves WHERE move=%s
        ''',('out'))
        allout =self.cur.fetchall()
        for row in allout:
            qout+=row[0]
        balance=qin-qout
        self.lineEdit_52.setText(str(balance))
        ##################show drawer balance
        qin1=0
        qout1=0
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('in'))
        allin =self.cur.fetchall()
        for row in allin:
            qin1+=row[0]
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('out'))
        allout =self.cur.fetchall()
        for row in allout:
            qout1+=row[0]
        balance=qin1-qout1
        self.lineEdit_58.setText(str(balance))
        
        self.get_safe_drawer_client()
        self.get_safe_drawer_vendor()
         ##########################auto compltete
        persons_list1=[]
        persons_list2=[]
        
        self.cur.execute('''SELECT name FROM clients''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list1.append(name[0])
        autocomplete(persons_list1,self.lineEdit_29)
        
        self.cur.execute('''SELECT name FROM vendors''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list2.append(name[0])
        autocomplete(persons_list2,self.lineEdit_31)
######################################################
    def show_employees(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_8.setCurrentIndex(1)
        self.comboBox_25.clear()
        self.dateEdit_9.setDate(datetime.date.today())
        self.cur.execute('''
            SELECT name FROM branch
            ''')
        branchs = self.cur.fetchall()
        for branch in branchs:
            self.comboBox_25.addItem(branch[0])
        
###########################################################
    def show_employees_absence_tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_8.setCurrentIndex(0)
        self.comboBox_28.clear()
        self.dateEdit_9.setDate(datetime.date.today())
       
        self.cur.execute('''
            SELECT name FROM employees
            ''')
        names = self.cur.fetchall()
        for name in names:
            self.comboBox_28.addItem(name[0])


##########################################################
    def show_sales(self):
        
        self.tabWidget.setCurrentIndex(5)
        self.cur.execute(''' SELECT id,name,amount,price,total,bill_id
                             FROM temp_bill WHERE move=%s''',('sell'))
        recover=self.cur.fetchall()
        if recover!=():
            total_bill=0
                    
            while self.tableWidget_3.rowCount()>0:
                self.tableWidget_3.removeRow(0)
                
            self.pushButton_51.setEnabled(True)
            
            for row , data in enumerate(recover):
                total_bill+=float(data[4])
                self.lineEdit_43.setText(str(total_bill))
                self.tableWidget_3.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(item)))
					
            self.cur.execute('''SELECT bill_id FROM temp_bill WHERE move=%s''',('sell'))
            bills=self.cur.fetchall()
            self.lineEdit_37.setText(str(bills[-1][0]))
            
        else:
            self.cur.execute('''SELECT number FROM bill_no''')
            nums=self.cur.fetchall()
            self.lineEdit_37.setText(str(int(nums[-1][0])+1))
        ##########################auto compltete
        items_list=[]
        persons_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_39)
        
        self.cur.execute('''SELECT name FROM clients''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list.append(name[0])
        autocomplete(persons_list,self.lineEdit_17)
        
            
###################################################
    def show_purchase(self):
        self.tabWidget.setCurrentIndex(7)

        qin1=0
        qout1=0
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('in'))
        allin =self.cur.fetchall()
        for row in allin:
            qin1+=row[0]
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('out'))
        allout =self.cur.fetchall()
        for row in allout:
            qout1+=row[0]
        balance=qin1-qout1
        self.lineEdit_107.setText(str(balance))
##########################
        self.cur.execute('''SELECT id,name,amount,price,total,bill_id
                         FROM temp_bill WHERE move=%s''',('pur'))
        recover=self.cur.fetchall()
        if recover!=():
            total_bill=0
            while self.tableWidget_5.rowCount()>0:
                self.tableWidget_5.removeRow(0)
            self.pushButton_58.setEnabled(True)
            for row , data in enumerate(recover):
                total_bill+=float(data[4])
                self.lineEdit_67.setText(str(total_bill))
                self.tableWidget_5.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_5.setItem(row,col,QTableWidgetItem(str(item)))
            self.cur.execute('''SELECT bill_id FROM temp_bill WHERE move=%s''',('pur'))
            bills=self.cur.fetchall()
            self.lineEdit_71.setText(str(bills[-1][0]))

            self.lineEdit_71.setText(str(int(recover[-1][5])+1))
        else:

            self.cur.execute('''SELECT number FROM bill_no''')
            nums=self.cur.fetchall()
            self.lineEdit_71.setText(str(int(nums[-1][0])+1))
        ###########################################    
        items_list=[]
        persons_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_63)
        
        self.cur.execute('''SELECT name FROM vendors''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list.append(name[0])
        autocomplete(persons_list,self.lineEdit_69)
        
#################################################################
    def show_report(self):
        self.tabWidget.setCurrentIndex(12)
##################################################
    def show_returnsales(self):
        self.tabWidget.setCurrentIndex(10)
        qin1=0
        qout1=0
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('in'))
        allin =self.cur.fetchall()
        for row in allin:
            qin1+=row[0]
        self.cur.execute('''
        SELECT amount FROM drawer_moves WHERE move=%s
        ''',('out'))
        allout =self.cur.fetchall()
        for row in allout:
            qout1+=row[0]
        balance=qin1-qout1
        self.lineEdit_106.setText(str(balance))
        ##############################################
        self.cur.execute('''SELECT id,name,amount,price,total,bill_id
                         FROM temp_bill WHERE move=%s''',('rsell'))
        recover=self.cur.fetchall()
        if recover!=():
            total_bill=0
            while self.tableWidget_4.rowCount()>0:
                self.tableWidget_4.removeRow(0)
            self.pushButton_53.setEnabled(True)
            for row , data in enumerate(recover):
                total_bill+=float(data[4])
                self.lineEdit_51.setText(str(total_bill))
                self.tableWidget_4.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))
            self.cur.execute('''SELECT bill_id FROM temp_bill WHERE move=%s''',('rsell'))
            bills=self.cur.fetchall()
            self.lineEdit_91.setText(str(bills[-1][0]))

            self.lineEdit_91.setText(str(int(recover[-1][5])+1))
        else:

            self.cur.execute('''SELECT number FROM bill_no''')
            nums=self.cur.fetchall()
            self.lineEdit_91.setText(str(int(nums[-1][0])+1))
        ###########################################    
        items_list=[]
        persons_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_46)
        
        self.cur.execute('''SELECT name FROM clients''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list.append(name[0])
        autocomplete(persons_list,self.lineEdit_57)
            
            
#################################show reports tabs
    def show_employee_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(0)
        self.comboBox_30.clear()
        self.comboBox_26.clear()
        self.dateEdit_15.setDate(datetime.date.today())
        self.dateEdit_16.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM employees''')
        emps=self.cur.fetchall()
        for i in emps:
            self.comboBox_30.addItem(i[0])
            
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for i in branchs:
            self.comboBox_26.addItem(i[0])
        
######################################################
                
    def show_expenses_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(1)
        self.dateEdit_18.setDate(datetime.date.today())
        self.dateEdit_19.setDate(datetime.date.today())
        while self.tableWidget_6.rowCount()>0:
            self.tableWidget_6.removeRow(0)
 #####################################################       
        
    def show_clven_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(2)
        self.dateEdit_20.setDate(datetime.date.today())
        self.dateEdit_21.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM clients''')
        clients=self.cur.fetchall()
        if clients==():
            pass
        else:
            for client in clients:
                self.comboBox_8.addItem(client[0])
        self.cur.execute('''SELECT name FROM vendors''')
        vendors=self.cur.fetchall()
        if vendors==():
            pass
        else:
            for vendor in vendors:
                self.comboBox_9.addItem(vendor[0])
##########################################################
        
    def show_itemsfast_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(3)
        self.comboBox.clear()
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox.addItem(branch[0])
        self.cur.execute('''SELECT name FROM depository''')
        depos=self.cur.fetchall()
        for depo in depos:
            self.comboBox.addItem(depo[0])
        ##########################auto compltete
        items_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_13)
        
        
##########################################################
        
    def show_itemsmovement_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(4)
        self.dateEdit_10.setDate(datetime.date.today())
        self.dateEdit_17.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox_14.addItem(branch[0])
        self.cur.execute('''SELECT name FROM depository''')
        depos=self.cur.fetchall()
        for depo in depos:
            self.comboBox_14.addItem(depo[0])
        ##########################auto compltete
        items_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_16)
   
######################################################
    def show_zeros_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(5)
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox_42.addItem(branch[0])
        self.cur.execute('''SELECT name FROM depository''')
        depos=self.cur.fetchall()
        for depo in depos:
            self.comboBox_42.addItem(depo[0])
########################################################
    def show_bill_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(6)
        self.dateEdit_12.setDate(datetime.date.today())
        self.dateEdit_33.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox_45.addItem(branch[0])
##########################################################
    def show_orderassold_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(7)
        self.dateEdit_13.setDate(datetime.date.today()-datetime.timedelta(days=1))
        self.dateEdit_34.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox_46.addItem(branch[0])
###########################################################
    def show_profit_reporttab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(8)
        self.dateEdit_14.setDate(datetime.date.today()-datetime.timedelta(days=1))
        self.dateEdit_35.setDate(datetime.date.today())
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        for branch in branchs:
            self.comboBox_47.addItem(branch[0])
##########################################################
    def show_barcode_tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_6.setCurrentIndex(9)
        self.cur.execute('''SELECT name FROM branch''')
        branchs=self.cur.fetchall()
        while self.tableWidget_25.rowCount()>0:
            self.tableWidget_25.removeRow(0)
        for branch in branchs:
            self.comboBox_48.addItem(branch[0])
        self.cur.execute('''SELECT barcode,name,amount FROM barcode_table''')
        datas=self.cur.fetchall()
        if datas==():
            pass
        else:
            for row,data in enumerate(datas):
                self.tableWidget_25.insertRow(row)
                for col,item in enumerate(data):
                    self.tableWidget_25.setItem(row,col,QTableWidgetItem(str(item)))
        ##########################auto compltete
        items_list=[]
        
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_20)
      
#########################################################
    def show_returnpur(self):
        self.tabWidget.setCurrentIndex(11)

        self.cur.execute('''SELECT id,name,amount,price,total,bill_id
                         FROM temp_bill WHERE move=%s''',('rpur'))
        recover=self.cur.fetchall()
        if recover!=():
            total_bill=0
            while self.tableWidget_9.rowCount()>0:
                self.tableWidget_9.removeRow(0)
            self.pushButton_73.setEnabled(True)
            for row , data in enumerate(recover):
                total_bill+=float(data[4])
                self.lineEdit_77.setText(str(total_bill))
                self.tableWidget_9.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_9.setItem(row,col,QTableWidgetItem(str(item)))

            self.lineEdit_103.setText(str(int(recover[-1][5])+1))
        else:

            self.cur.execute('''SELECT number FROM bill_no''')
            nums=self.cur.fetchall()
            self.lineEdit_103.setText(str(int(nums[-1][0])+1))
        ###########################################    
        items_list=[]
        persons_list=[]
        
        self.cur.execute('''SELECT name FROM items''')
        names=self.cur.fetchall() 
        for name in names:
            items_list.append(name[0])
        autocomplete(items_list,self.lineEdit_73)
        
        self.cur.execute('''SELECT name FROM vendors''')
        names=self.cur.fetchall() 
        for name in names:
            persons_list.append(name[0])
        autocomplete(persons_list,self.lineEdit_97)
#####################################
    
####################################items tab

    def item_find(self):##################find item to edit its information
        name=self.lineEdit.text()
        barcode=self.lineEdit_5.text()
        self.lineEdit.setEnabled(False)
        self.lineEdit_5.setEnabled(False)
        self.pushButton_13.setEnabled(True)
        self.pushButton_17.setEnabled(True)
        if name==''and barcode=='':
            QMessageBox.about(self,'caution','inter name or barcode to search')
            self.lineEdit.setEnabled(True)
            self.lineEdit_5.setEnabled(True)
            self.pushButton_13.setEnabled(False)
        elif name!=''and barcode=='':
            self.cur.execute('''
            SELECT * FROM items WHERE name=%s
            ''',(name))
            item=self.cur.fetchall()
            if item==():
                QMessageBox.about(self,'caution','item not found')
                self.pushButton_13.setEnabled(False)
                self.lineEdit.setEnabled(True)
                self.lineEdit_5.setEnabled(True)
            else:
                self.lineEdit_2.setText(str(item[0][2]))
                self.lineEdit_3.setText(str(item[0][3]))
                self.lineEdit_4.setText(str(item[0][4]))
                self.lineEdit_5.setText(item[0][5])
                self.lineEdit_21.setText(str(item[0][6]))
                self.textEdit_9.setText(item[0][7])
                self.pushButton_14.setEnabled(False)

        elif name==''and barcode!='':
            self.cur.execute('''
            SELECT * FROM items WHERE barcode=%s
            ''',(barcode))
            item=self.cur.fetchall()
            if item==():
                QMessageBox.about(self,'caution','item not found')
                self.lineEdit.setEnabled(True)
                self.lineEdit_5.setEnabled(True)
                self.pushButton_13.setEnabled(False)
            else:
                self.lineEdit.setText(str(item[0][1]))
                self.lineEdit_2.setText(str(item[0][2]))
                self.lineEdit_3.setText(str(item[0][3]))
                self.lineEdit_4.setText(str(item[0][4]))
                self.lineEdit_21.setText(str(item[0][6]))
                self.textEdit_9.setText(str(item[0][7]))

        elif name!=''and barcode!='':
            QMessageBox.about(self,'caution','search by name or barcode')
            self.lineEdit.setEnabled(True)
            self.lineEdit_5.setEnabled(True)
            self.pushButton_13.setEnabled(False)
###################################################
    def item_edit(self):##################edit found item
        pur_price=self.lineEdit_2.text()
        sell_price=self.lineEdit_3.text()
        fast_code=self.lineEdit_4.text()
        req_quan=self.lineEdit_21.text()
        comment=self.textEdit.toPlainText()
        barcode=self.lineEdit_5.text()
        self.pushButton_13.setEnabled(False)
        self.lineEdit.setEnabled(True)
        self.lineEdit_5.setEnabled(True)

        if pur_price =='' or sell_price =='' or req_quan == '':
            QMessageBox.about(self, 'caution', 'prices, quantity is mandatory')
        elif not isfloat(pur_price) or not isfloat(sell_price) or not isint(req_quan):
            QMessageBox.about(self, 'caution','check for numbers')
        else:
            self.cur.execute('''
            UPDATE items SET pur_price=%s,sell_price=%s,fast_code=%s,
            req_quan=%s,comment=%s WHERE barcode=%s
            ''',(pur_price,sell_price,fast_code,req_quan,comment,barcode))
            self.db.commit()
            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_21.setText('')
            self.textEdit_9.setText('')
            self.pushButton.setEnabled(False)
            #print ('success')
######################################################
    def item_new(self):###########start screen over
        self.pushButton_13.setEnabled(False)
        self.lineEdit.setEnabled(True)
        self.lineEdit_5.setEnabled(True)
        self.lineEdit.setText('')
        self.lineEdit_2.setText('')
        self.lineEdit_3.setText('')
        self.lineEdit_4.setText('')
        self.lineEdit_5.setText('')
        self.lineEdit_21.setText('')
        self.textEdit_9.setText('')
        self.pushButton_14.setEnabled(True)
####################################################
    def item_save(self):##################save new item or save the editing
        name=self.lineEdit.text()
        pur_price=self.lineEdit_2.text()
        sell_price=self.lineEdit_3.text()
        fast_code=self.lineEdit_4.text()
        barcode=self.lineEdit_5.text()
        req_quant=self.lineEdit_21.text()
        comment=self.textEdit.toPlainText()
        have_expiry=self.checkBox.isChecked()
        quantity=0

        self.cur.execute(''' SELECT name FROM items
         WHERE name=%s''',(name))
        x=self.cur.fetchall()

        self.cur.execute(''' SELECT barcode FROM items
         WHERE barcode=%s''',(barcode))
        y=self.cur.fetchall()

        if name =='' or pur_price =='' or sell_price =='' or req_quant == '':
            QMessageBox.about(self, 'caution', 'name, prices, quantity is mandatory')
        elif x !=():
            QMessageBox.about(self, 'caution', 'name already exist')
        elif y !=():
            QMessageBox.about(self, 'caution', 'barcode already exist')
        elif not isfloat(pur_price) or not isfloat(sell_price) or not isint(req_quant):
            QMessageBox.about(self, 'caution','check for numbers')
        else:
            self.cur.execute('''
            INSERT INTO items(name,pur_price,sell_price,
            fast_code, barcode, req_quan, comment, have_expiry)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name, pur_price, sell_price,
                fast_code,barcode,req_quant,comment,have_expiry))
            self.db.commit()

            self.lineEdit.setText('')
            self.lineEdit_2.setText('')
            self.lineEdit_3.setText('')
            self.lineEdit_4.setText('')
            self.lineEdit_5.setText('')
            self.lineEdit_21.setText('')
            self.textEdit.setText('')

            #print('success')
############################################
    def stockedit_startover(self):
        self.lineEdit_27.setEnabled(False)
        self.pushButton_37.setEnabled(False)
        self.pushButton_35.setEnabled(False)
        self.lineEdit_34.setEnabled(True)
        self.lineEdit_27.setText('')
        self.lineEdit_34.setText('')
        self.lineEdit_9.setText('')

#####################################################
    def stockedit_show(self):##################show item balance to edit stock

        name=self.lineEdit_34.text()
        store=self.comboBox_16.currentText()
        qin=0
        qout=0
        self.cur.execute('''SELECT name FROM items WHERE name=%s
                        ''',(name))
        check=self.cur.fetchall()
        if self.lineEdit_34.text() =='':
            QMessageBox.about(self, 'caution', 'name is mandatory')
        else:

            self.cur.execute('''SELECT quantity FROM item_quant
                                WHERE name=%s AND store=%s
                            ''',(name,store))
            quant=self.cur.fetchall()
            if quant!=():
                self.lineEdit_9.setText(str(quant[0][0]))
                self.lineEdit_27.setEnabled(True)
                self.pushButton_37.setEnabled(True)
                self.pushButton_35.setEnabled(True)
                self.lineEdit_34.setEnabled(False)
            elif quant==():
                if check==():
                    QMessageBox.about(self, 'caution', 'item not found')
                    self.lineEdit_9.setText('')
                else:
                    self.lineEdit_9.setText('0')
                    self.lineEdit_27.setEnabled(True)
                    self.pushButton_37.setEnabled(True)
                    self.pushButton_35.setEnabled(True)
                    self.lineEdit_34.setEnabled(False)
            #print ('success')
##############################################################
    def stockedit_remove(self):##################remove amount from stock

        name=self.lineEdit_34.text()
        reason=self.comboBox_11.currentText()
        amount=self.lineEdit_27.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        balance=self.lineEdit_9.text()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        store=self.comboBox_16.currentText()
        price=0

        if self.lineEdit_34.text()==''or self.lineEdit_27.text() ==''or self.lineEdit_9.text()=='':
            QMessageBox.about(self, 'caution', 'name, amount is mandatory')
        elif not isfloat(amount):
            QMessageBox.about(self, 'caution', 'inter digits only')
            self.lineEdit_27.setFocus()
            self.lineEdit_27.setText('')
        elif amount>balance:
            QMessageBox.about(self, 'caution', 'amount greater than your balance')
        
            

        else:

            self.cur.execute('''
               INSERT INTO items_moves(name, amount, date, time, employee, store1,move,operation,reason)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ''',(name,amount,date,time,employee,store,'out','edit',reason))
            self.db.commit()

            self.cur.execute('''SELECT name, quantity FROM item_quant
            WHERE name=%s AND store=%s''',(name,store))
            check=self.cur.fetchall()
            if check==():
                self.cur.execute('''
                INSERT INTO item_quant(name,quantity,store)
                VALUES(%s,%s,%s)
                ''',(name,amount,store))
                self.db.commit()
            elif check != ():
                quantity=float(check[0][1])-float(amount)
                self.cur.execute('''UPDATE item_quant SET quantity=%s
                 WHERE name=%s AND store=%s
            ''',(quantity,name,store))
            self.db.commit()
            self.lineEdit_27.setEnabled(False)
            self.pushButton_37.setEnabled(False)
            self.pushButton_35.setEnabled(False)
            self.lineEdit_34.setEnabled(True)
            self.lineEdit_27.setText('')
            self.lineEdit_34.setText('')
            self.lineEdit_9.setText('')

            #print('success')
##########################################################

    def stockedit_add(self):##################add amount to stock
        name=self.lineEdit_34.text()
        move='in'
        reason=self.comboBox_11.currentText()
        operation='edit'
        amount=self.lineEdit_27.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        store=self.comboBox_16.currentText()
        price=0
        if self.lineEdit_34.text()==''or self.lineEdit_27.text()==''or self.lineEdit_9.text()=='':
            QMessageBox.about(self, 'caution', 'name, amount is mandatory')
        elif not isfloat(amount):
            QMessageBox.about(self, 'caution', 'inter digits only')
            self.lineEdit_27.setFocus()
            self.lineEdit_27.setText('')
        else:
            self.cur.execute('''
               INSERT INTO items_moves(name, amount, date, time, employee, store1,move,operation,reason)
               VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
               ''',(name,amount,date,time,employee,store,'in','edit',reason))
            self.db.commit()
            self.cur.execute('''SELECT name, quantity FROM item_quant
            WHERE name=%s AND store=%s''',(name,store))
            check=self.cur.fetchall()
            if check==():
                self.cur.execute('''
                INSERT INTO item_quant(name,quantity,store)
                VALUES(%s,%s,%s)
                ''',(name,amount,store))
                self.db.commit()
            elif check != ():
                quantity=float(check[0][1])+float(amount)
                self.cur.execute('''UPDATE item_quant SET quantity=%s
                 WHERE name=%s AND store=%s
            ''',(quantity,name,store))
            self.db.commit()

            self.lineEdit_27.setEnabled(False)
            self.lineEdit_27.setText('')
            self.pushButton_37.setEnabled(False)
            self.pushButton_35.setEnabled(False)
            self.lineEdit_34.setEnabled(True)
            self.lineEdit_34.setText('')
            self.lineEdit_9.setText('')

            #print('success')
############################################
    def stockmove_show(self):##################show item balance to move stock
        name=self.lineEdit_56.text()
        store1=self.comboBox_19.currentText()
        store2=self.comboBox_20.currentText()

        self.cur.execute('''SELECT name FROM items WHERE name=%s
                        ''',(name))
        check=self.cur.fetchall()
########################first store
        if self.lineEdit_56.text() =='':
            QMessageBox.about(self, 'caution', 'name is mandatory')

        elif check==():
            QMessageBox.about(self, 'caution', 'item not found')

        else:
            self.cur.execute('''SELECT quantity FROM item_quant
                                WHERE name=%s AND store=%s
                            ''',(name,store1))
            quant1=self.cur.fetchall()
            self.cur.execute('''SELECT quantity FROM item_quant
                                WHERE name=%s AND store=%s
                            ''',(name,store2))
            quant2=self.cur.fetchall()
            if quant1==():
                self.lineEdit_26.setText('0')
            else:
                self.lineEdit_26.setText(str(quant1[0][0]))

            if quant2==():
                self.lineEdit_7.setText('0')
            else:
                self.lineEdit_7.setText(str(quant2[0][0]))


            self.lineEdit_56.setEnabled(False)
            self.lineEdit_28.setEnabled(True)
            self.pushButton_41.setEnabled(True)


          #  print ('success')
###############################################
    def stockmove_move(self):##################move amount from store to another

        name= self.lineEdit_56.text()
        amount=self.lineEdit_28.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        balance1=self.lineEdit_26.text()
        store1=self.comboBox_19.currentText()
        store2=self.comboBox_20.currentText()

        if self.lineEdit_56.text()=='' or self.lineEdit_28.text()=='':
            QMessageBox.about(self, 'caution', 'name and amount is mandatory')
        elif not isfloat(amount):
            QMessageBox.about(self, 'caution', 'inter digits only')
            self.lineEdit_28.setFocus()
            self.lineEdit_28.setText('')
        elif store1==store2:
            QMessageBox.about(self, 'caution', 'choose different stores')
        elif float(amount) > float(balance1):
            QMessageBox.about(self,'caution', 'amount is greater the balance')
        elif self.lineEdit_26.text()=='':
                QMessageBox.about(self, 'caution','item not found in source store')
        else:

            self.cur.execute('''
            INSERT INTO items_moves(name, amount, date, time, employee, store1,store2,operation)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name,amount,date,time,employee,store1,store2,'move'))
            self.db.commit()
            ###################
            # self.cur.execute('''
            # INSERT INTO items_moves(name, amount, date, time, employee, store,move,operation)
            # VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            # ''',(name,amount,date,time,employee,store2,'in','move'))
            # self.db.commit()
            ####################
            self.cur.execute('''SELECT name, quantity FROM item_quant
            WHERE name=%s AND store=%s''',(name,store1))
            check1=self.cur.fetchall()

            self.cur.execute('''SELECT name, quantity FROM item_quant
            WHERE name=%s AND store=%s''',(name,store2))
            check2=self.cur.fetchall()

            quantity1=float(check1[0][1])-float(amount)
            self.cur.execute('''UPDATE item_quant SET quantity=%s
             WHERE name=%s AND store=%s
        ''',(quantity1,name,store1))

            if check2==():
                self.cur.execute('''
                INSERT INTO item_quant(name,quantity,store)
                VALUES(%s,%s,%s)
                ''',(name,amount,store2))
                self.db.commit()
            elif check2 != ():
                quantity2=float(check2[0][1])+float(amount)
                self.cur.execute('''UPDATE item_quant SET quantity=%s
                 WHERE name=%s AND store=%s
            ''',(quantity2,name,store2))
            self.db.commit()

            self.lineEdit_56.setText('')
            self.lineEdit_28.setText('')
            self.lineEdit_26.setText('')
            self.lineEdit_7.setText('')
            self.lineEdit_56.setEnabled(True)
            self.lineEdit_28.setEnabled(False)
            self.pushButton_41.setEnabled(False)
         #   print('success')

#####################################
    def stockmove_startover(self):
        self.lineEdit_56.setText('')
        self.lineEdit_28.setText('')
        self.lineEdit_26.setText('')
        self.lineEdit_7.setText('')
        self.lineEdit_56.setEnabled(True)
        self.lineEdit_28.setEnabled(False)
        self.pushButton_41.setEnabled(False)
##################################### clients and vendors tab

    def client_find(self):##################find client to edit info
        name=self.lineEdit_14.text()
        phone=self.lineEdit_60.text()
        self.pushButton_21.setEnabled(False)
        if name=='' and phone=='':
            QMessageBox.about(self,'caution','inter name or phone')
            self.pushButton_21.setEnabled(True)
        elif name!='' and phone=='':
            self.cur.execute('''SELECT  phone, comment
            FROM clients WHERE name=%s
            ''',(name))
            client=self.cur.fetchall()
            if client==():
                QMessageBox.about(self,'caution','client not found')
            else:
                self.lineEdit_14.setEnabled(False)
                self.lineEdit_60.setText(client[0][0])
                self.textEdit_6.setText(client[0][1])
                self.pushButton_42.setEnabled(True)
        elif name=='' and phone !='':
            self.cur.execute('''SELECT  name, comment
            FROM clients WHERE phone=%s
            ''',(phone))
            client=self.cur.fetchall()
            if client==():
                QMessageBox.about(self,'caution','client not found')
            else:
                self.lineEdit_60.setEnabled(False)
                self.lineEdit_14.setEnabled(False)
                self.lineEdit_14.setText(client[0][0])
                self.textEdit_6.setText(client[0][1])
                self.pushButton_42.setEnabled(True)

              #  print('success')
################################################
    def client_edit(self):
        name=self.lineEdit_14.text()
        phone=self.lineEdit_60.text()
        comment=self.textEdit_6.toPlainText()
        self.cur.execute('''
            UPDATE clients SET phone=%s,comment=%s WHERE name=%s
            ''',(phone,comment,name))
        self.db.commit()
        self.lineEdit_14.setEnabled(True)
        self.lineEdit_60.setEnabled(True)
        self.textEdit_6.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_60.setText('')
        self.pushButton_21.setEnabled(True)
        self.pushButton_42.setEnabled(False)


#########################################
    def client_new(self):########start screen over
        self.lineEdit_14.setEnabled(True)
        self.lineEdit_60.setEnabled(True)
        self.textEdit_6.setText('')
        self.lineEdit_14.setText('')
        self.lineEdit_60.setText('')
        self.pushButton_21.setEnabled(True)
        self.pushButton_42.setEnabled(False)
###################################################
    def client_save(self):##################save new client or save editing
        name=self.lineEdit_14.text()
        phone=self.lineEdit_60.text()
        comment=self.textEdit_6.toPlainText()
        self.cur.execute(''' SELECT name FROM clients WHERE name=%s
        ''',(name))
        x=self.cur.fetchall()

        if name =='' :
            QMessageBox.about(self,'caution', 'name is mandatory')
        elif x !=():
            QMessageBox.about(self,'caution', 'name already exist')
        else:
            self.cur.execute('''
            INSERT INTO clients(name,phone,comment)
            VALUES(%s,%s,%s)
            ''',(name,phone,comment))
            self.db.commit()
            self.cur.execute('''INSERT INTO client_balance(name,amount,move)
            VALUES(%s,%s,%s)
            ''',(name,0,'in'))
            self.cur.execute('''INSERT INTO client_balance(name,amount,move)
            VALUES(%s,%s,%s)
            ''',(name,0,'out'))
            self.db.commit()
            self.lineEdit_14.setText('')
            self.textEdit_6.setText('')
            self.lineEdit_60.setText('')

         #   print('success')
##############################################
    def vendor_find(self):##################find vendor to edit info
        name=self.lineEdit_15.text()
        phone=self.lineEdit_59.text()
        self.pushButton_22.setEnabled(False)
        if name=='' and phone=='':
            QMessageBox.about(self,'caution','inter name or phone')
            self.pushButton_22.setEnabled(True)
        elif name!='' and phone=='':
            self.cur.execute('''SELECT  phone, comment
            FROM vendors WHERE name=%s
            ''',(name))
            vendor=self.cur.fetchall()
            if vendor==():
                QMessageBox.about(self,'caution','vendor not found')
            else:
                self.lineEdit_15.setEnabled(False)
                self.lineEdit_59.setText(vendor[0][0])
                self.textEdit_7.setText(vendor[0][1])
                self.pushButton_26.setEnabled(True)
               # print('success')
        elif name=='' and phone !='':
            self.cur.execute('''SELECT  name, comment
            FROM vendors WHERE phone=%s
            ''',(phone))
            vendor=self.cur.fetchall()
            if vendor==():
                QMessageBox.about(self,'caution','vendor not found')
            else:
                self.lineEdit_59.setEnabled(False)
                self.lineEdit_15.setEnabled(False)
                self.lineEdit_15.setText(vendor[0][0])
                self.textEdit_7.setText(vendor[0][1])
                self.pushButton_26.setEnabled(True)

              #  print('success')
#########################################
    def vendor_new(self):############start screen over
        self.lineEdit_15.setEnabled(True)
        self.lineEdit_59.setEnabled(True)
        self.textEdit_7.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_59.setText('')
        self.pushButton_22.setEnabled(True)
        self.pushButton_26.setEnabled(False)
###############################################
    def vendor_edit(self):
        name=self.lineEdit_15.text()
        phone=self.lineEdit_59.text()
        comment=self.textEdit_7.toPlainText()
        self.cur.execute('''
            UPDATE vendors SET phone=%s,comment=%s WHERE name=%s
            ''',(phone,comment,name))
        self.db.commit()

        self.lineEdit_15.setEnabled(True)
        self.lineEdit_59.setEnabled(True)
        self.textEdit_7.setText('')
        self.lineEdit_15.setText('')
        self.lineEdit_59.setText('')
        self.pushButton_22.setEnabled(True)
        self.pushButton_26.setEnabled(False)
##############################################
    def vendor_save(self):##################save new vendor or save editing
        name=self.lineEdit_15.text()
        phone=self.lineEdit_59.text()
        comment=self.textEdit_7.toPlainText()
        self.cur.execute(''' SELECT name FROM vendors WHERE name=%s
        ''',(name))
        x=self.cur.fetchall()
        if name =='':
            QMessageBox.about(self,'caution','name is mandatory')
        elif x !=():
            QMessageBox.about(self,'caution', 'name already exist')
        else:
            self.cur.execute('''
            INSERT INTO vendors(name,phone,comment)
            VALUES(%s,%s,%s)
            ''',(name,phone,comment))
            self.db.commit()
            self.cur.execute('''INSERT INTO vendor_balance(name,amount,move)
            VALUES(%s,%s,%s)
            ''',(name,0,'in'))
            self.cur.execute('''INSERT INTO vendor_balance(name,amount,move)
            VALUES(%s,%s,%s)
            ''',(name,0,'out'))
            self.db.commit()


            self.lineEdit_15.setText('')
            self.textEdit_7.setText('')
            self.lineEdit_59.setText('')

           # print('success')

#####################################

##################################### stores and branchs tab

  
###################################################
    def depository_save(self):##################save the new or editing
        name=self.lineEdit_11.text()
        branch=self.comboBox_17.currentText()
        comment=self.textEdit_3.toPlainText()
        self.cur.execute(''' SELECT name FROM depository WHERE name=%s
        ''',(name))
        x=self.cur.fetchall()

        if name=='':
            QMessageBox.about(self,'caution','name is mandatory')
        elif x != ():
            QMessageBox.about(self,'caution','name already exist')
        else:
            self.cur.execute('''
            INSERT INTO depository(name,belong,comment)
            VALUES(%s,%s,%s)
            ''',(name,branch,comment))
            self.db.commit()

            self.lineEdit_11.setText('')
            self.textEdit_3.setText('')

            #('success')
############################################

###############################################
    def branch_save(self):##################save new or the edit
        name=self.lineEdit_12.text()
        comment=self.textEdit_4.toPlainText()
        self.cur.execute(''' SELECT name FROM branch WHERE name=%s
        ''',(name))
        x=self.cur.fetchall()
        if name=='':
            QMessageBox.about(self,'caution','name is mandatory')
        if x!=():
            QMessageBox.about(self,'caution','name already exist')
        else:
            self.cur.execute('''
            INSERT INTO branch(name,comment)
            VALUES(%s,%s)
            ''',(name,comment))
            self.db.commit()

            self.lineEdit_12.setText('')
            self.textEdit_4.setText('')


#####################################

#####################################finance tab

    def safe_move_money_out(self):##################save money move from safe
        self.cur.execute('''
            SELECT branch FROM default_branch
            ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        reason=self.comboBox_15.currentText()
        amount=self.lineEdit_32.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        comment=self.textEdit_10.toPlainText()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        if self.lineEdit_32.text()=='':
            QMessageBox.about(self, 'caution', 'inter money amount')
        elif not isfloat(amount):
            QMessageBox.about(self,'cuation','inter numbers only')
        elif float(self.lineEdit_52.text())<float(amount):
            QMessageBox.about(self,'caution','balance in not enought')
        else:
            self.cur.execute('''
            INSERT INTO safe_moves(branch,reason,amount,date,time,
            comment,employee,move,source)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(branch,reason,amount,date,time,comment,employee,'out','transfer'))
            self.db.commit()
            if self.comboBox_15.currentIndex()==0:
                self.cur.execute('''
                INSERT INTO drawer_moves(branch,reason,amount,date,time,
                comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',(branch,'from safe',amount,date,time,comment,employee,'in','transfer'))
                self.db.commit()
            self.lineEdit_32.setText('')
            self.textEdit_10.setText('')
           # print('success')
################################################
    def safe_move_money_in(self):##################save money move from safe
        self.cur.execute('''
            SELECT branch FROM default_branch
            ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        reason=self.comboBox_15.currentText()
        amount=self.lineEdit_32.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        comment=self.textEdit_10.toPlainText()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        if self.lineEdit_32.text()=='':
            QMessageBox.about(self, 'caution', 'inter money amount')
        elif not isfloat(amount):
            QMessageBox.about(self,'cuation','inter numbers only')


        elif self.comboBox_15.currentIndex() != 2:
            QMessageBox.about(self,'caution','reason must be owner')
        else:
            self.cur.execute('''
            INSERT INTO safe_moves(branch,reason,amount,date,time,
            comment,employee,move,source)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(branch,reason,amount,date,time,comment,employee,'in','transfer'))
            self.db.commit()
           
            self.lineEdit_32.setText('')
            self.textEdit_10.setText('')
##################################################

    def drawer_move_money(self):##################save money move from drawer
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        reason=self.comboBox_21.currentText()
        amount=self.lineEdit_30.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        comment=self.textEdit_11.toPlainText()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        if self.lineEdit_30.text()=='':
            QMessageBox.about(self, 'caution', 'inter money amount')
        elif not isfloat(amount):
            QMessageBox.about(self,'caution','inter numbers only')
        elif float(self.lineEdit_58.text())<float(amount):
            QMessageBox.about(self,'caution','balance is not enough')
        else:
            self.cur.execute('''
            INSERT INTO drawer_moves(branch,reason,amount,date,time,
            comment,employee,move,source)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(branch,reason,amount,date,time,comment,employee,'out','transfer'))
            self.db.commit()
            if self.comboBox_21.currentIndex()==0:
                self.cur.execute('''
                INSERT INTO safe_moves(branch,reason,amount,date,time,
                comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',(branch,'from drawer',amount,date,time,comment,employee,'in','transfer'))
                self.db.commit()
            self.lineEdit_30.setText('')
            self.textEdit_11.setText('')
            #print('success')
#############################################################################

    def clven_startover(self):################start screen over
            self.lineEdit_29.setText('')
            self.lineEdit_22.setText('')
            self.lineEdit_23.setText('')
            self.lineEdit_29.setEnabled(True)
            self.lineEdit_23.setEnabled(False)
            self.pushButton_31.setEnabled(False)
            self.pushButton_15.setEnabled(False)
            self.lineEdit_31.setText('')
            self.lineEdit_25.setText('')
            self.lineEdit_24.setText('')
            self.lineEdit_31.setEnabled(True)
            self.lineEdit_24.setEnabled(False)
            self.pushButton_48.setEnabled(False)
            self.pushButton_24.setEnabled(False)

####################################################
    def client_show_balance(self):##################show client balance
        name=self.lineEdit_29.text()
        moin=0
        mout=0
        if name=='':
            QMessageBox.about(self,'caution','inter client name')
        else:
            self.cur.execute('''SELECT amount FROM client_balance
            WHERE name=%s AND move=%s
            ''',(name,'in'))
            allin=self.cur.fetchall()
            for row in allin:
                moin+=int(row[0])
            if allin==():
                QMessageBox.about(self,'caution','client not found')
                self.lineEdit_23.setEnabled(False)
                self.pushButton_15.setEnabled(False)
                self.pushButton_31.setEnabled(False)
            else:
                self.cur.execute('''SELECT amount FROM client_balance
                WHERE name=%s AND move=%s
                ''',(name,'out'))
                allout=self.cur.fetchall()
                for row in allout:
                    mout+=int(row[0])
                self.lineEdit_23.setEnabled(True)
                self.pushButton_15.setEnabled(True)
                self.pushButton_31.setEnabled(True)
                self.lineEdit_29.setEnabled(False)
                balance=mout-moin
                self.lineEdit_22.setText(str(balance))

####################################################
    def client_take_money(self):##################take money from client
        name=self.lineEdit_29.text()
        amount=self.lineEdit_23.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        balance=self.lineEdit_111.text()
        comment=self.textEdit_13.toPlainText()
        if amount=='' or not isfloat(amount):
            QMessageBox.about(self,'caution','inter correct money')
        
        else:
            self.cur.execute('''INSERT INTO client_balance(name,
            amount,date,time,move,reason,employee,branch)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name,amount,date,time,'in','transfer',employee,branch))
            self.db.commit()
            if self.comboBox_10.currentText() == 'SAFE':
                self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'client',amount,date,time,comment,employee,'in',name))
                self.db.commit()
            else:
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'client',amount,date,time,comment,employee,'in',name))
                self.db.commit()
                
        
            self.lineEdit_29.setEnabled(True)
            self.lineEdit_29.setText('')
            self.lineEdit_23.setEnabled(False)
            self.lineEdit_23.setText('')
            self.lineEdit_22.setText('')
            self.pushButton_31.setEnabled(False)
            self.pushButton_15.setEnabled(False)

#######################################
    def client_give_money(self):##################give money to the client
        name=self.lineEdit_29.text()
        amount=self.lineEdit_23.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        balance=self.lineEdit_111.text()
        comment=self.textEdit_13.toPlainText()
        if amount=='' or not isfloat(amount):
            QMessageBox.about(self,'caution','inter correct money')
        elif amount > balance:
            QMessageBox.about(self,'caution','balance is not enough')
        else:
            self.cur.execute('''INSERT INTO client_balance(name,
            amount,date,time,move,reason,employee,branch)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name,amount,date,time,'out','transfer',employee,branch))
            self.db.commit()
            
            if self.comboBox_10.currentText() == 'SAFE':
                self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'client',amount,date,time,comment,employee,'out',name))
                self.db.commit()
            else:
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'client',amount,date,time,comment,employee,'out',name))
                self.db.commit()
            
            self.lineEdit_29.setEnabled(True)
            self.lineEdit_29.setText('')
            self.lineEdit_23.setEnabled(False)
            self.lineEdit_23.setText('')
            self.lineEdit_22.setText('')
            self.pushButton_31.setEnabled(False)
            self.pushButton_15.setEnabled(False)

#####################################################
    def vendor_show_balance(self):##################show client balance
        name=self.lineEdit_31.text()
        moin=0
        mout=0
        if name=='':
            QMessageBox.about(self,'caution','inter vendor name')
        else:
            self.cur.execute('''SELECT amount FROM vendor_balance
            WHERE name=%s AND move=%s
            ''',(name,'in'))
            allin=self.cur.fetchall()
            for row in allin:
                moin+=int(row[0])
            if allin==():
                QMessageBox.about(self,'caution','vendor not found')
                self.lineEdit_24.setEnabled(False)
                self.pushButton_48.setEnabled(False)
                self.pushButton_24.setEnabled(False)
            else:
                self.cur.execute('''SELECT amount FROM vendor_balance
                WHERE name=%s AND move=%s
                ''',(name,'out'))
                allout=self.cur.fetchall()
                for row in allout:
                    mout+=int(row[0])
                self.lineEdit_24.setEnabled(True)
                self.pushButton_48.setEnabled(True)
                self.pushButton_24.setEnabled(True)
                self.lineEdit_31.setEnabled(False)
                balance=moin-mout
                self.lineEdit_25.setText(str(balance))

######################################################
    def vendor_take_money(self):##################take money from client
        name=self.lineEdit_31.text()
        amount=self.lineEdit_24.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        balance=self.lineEdit_112.text()
        comment=self.textEdit_14.toPlainText()
        if amount=='' or not isfloat(amount):
            QMessageBox.about(self,'caution','inter correct money')
        else:
            self.cur.execute('''INSERT INTO vendor_balance(name,
            amount,date,time,move,reason,employee,branch)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name,amount,date,time,'in','transfer',employee,branch))
            self.db.commit()
            
            if self.comboBox_12.currentText() == 'SAFE':
                self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'vendor',amount,date,time,comment,employee,'in',name))
                self.db.commit()
            else:
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'vendor',amount,date,time,comment,employee,'in',name))
                self.db.commit()
            self.lineEdit_31.setEnabled(True)
            self.lineEdit_31.setText('')
            self.lineEdit_24.setEnabled(False)
            self.lineEdit_24.setText('')
            self.lineEdit_25.setText('')
            self.pushButton_48.setEnabled(False)
            self.pushButton_24.setEnabled(False)

####################################################
    def vendor_give_money(self):##################give money to the client
        name=self.lineEdit_31.text()
        amount=self.lineEdit_24.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        balance=self.lineEdit_112.text()
        comment=self.textEdit_14.toPlainText()
        if amount=='' or not isfloat(amount):
            QMessageBox.about(self,'caution','inter correct money')
        elif amount > balance:
            QMessageBox.about(self,'caution','balance is not enough')
        else:
            self.cur.execute('''INSERT INTO vendor_balance(name,
            amount,date,time,move,reason,employee,branch)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            ''',(name,amount,date,time,'out','transfer',employee,branch))
            self.db.commit()
            
            if self.comboBox_12.currentText() == 'SAFE':
                self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'vendor',amount,date,time,comment,employee,'out',name))
                self.db.commit()
            else:
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(branch, 'vendor',amount,date,time,comment,employee,'out',name))
                self.db.commit()
                
            self.lineEdit_31.setEnabled(True)
            self.lineEdit_31.setText('')
            self.lineEdit_24.setEnabled(False)
            self.lineEdit_24.setText('')
            self.lineEdit_25.setText('')
            self.pushButton_48.setEnabled(False)
            self.pushButton_24.setEnabled(False)

#####################################

#####################################employees tab

    
#################################################
    def employee_save(self):#save editing or new
        name=self.lineEdit_33.text()
        password=self.lineEdit_55.text()
        branch=self.comboBox_25.currentText()
        dedication=self.comboBox_3.currentText()
        adminity=self.comboBox_27.currentText()
        date=self.dateEdit_9.text()
        comment=self.textEdit_5.toPlainText()
        auth1=self.checkBox_1.isChecked()
        auth2=self.checkBox_2.isChecked()
        auth3=self.checkBox_3.isChecked()
        auth4=self.checkBox_4.isChecked()
        auth5=self.checkBox_5.isChecked()
        auth6=self.checkBox_6.isChecked()
        auth7=self.checkBox_7.isChecked()
        auth8=self.checkBox_8.isChecked()
        auth9=self.checkBox_9.isChecked()
        auth10=self.checkBox_10.isChecked()
        auth11=self.checkBox_11.isChecked()
        
        if name =='' or password=='':
            QMessageBox.about(self,'caution','name and password is mandatory')
        else:

            self.cur.execute('''SELECT name FROM employees WHERE name=%s''',(name))
            check=self.cur.fetchall()
            if check!=():
                QMessageBox.about(self,'caution''there is already the same name')
            else:
                self.cur.execute('''
                INSERT INTO employees(name,password,branch,
                dedicate, adminity, join_date, comment,auth1,auth2,auth3,auth4,auth5,auth6,auth7,auth8,auth9,auth10,auth11)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',(name,password,branch,dedication,adminity,date,comment,auth1,auth2,auth3,auth4,auth5,auth6,auth7,auth8,auth9,auth10,auth11))
                self.db.commit()

                self.lineEdit_33.setText('')
                self.lineEdit_55.setText('')
                self.textEdit_5.setText('')

###################################################
    def employee_leaving(self):#save date and time of employee comming
        name=self.comboBox_28.currentText()
        comment=' <> '+ self.textEdit_15.toPlainText()
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''SELECT date, time_in, time_out, comment FROM employee_absence WHERE date=%s AND name=%s''',(date,name))
        day=self.cur.fetchall()
        
        if day==():
            QMessageBox.about(self,'hint','this employee didnt come today')
        elif day[-1][2]!=None:
            
            QMessageBox.about(self,'hint','this employee already leaved')
        else:
            timein=day[-1][1]
            self.cur.execute('''UPDATE employee_absence SET time_out=%s, comment=%s
                     WHERE name=%s AND date=%s AND time_in=%s''',(time,day[-1][3]+comment,name,date,timein))
            self.db.commit()
            self.textEdit_15.setText('')
            QMessageBox.about(self,'hint','done')
############################################################
    def employee_comming(self):#save date and time of employee leaving
        name=self.comboBox_28.currentText()
        comment=self.textEdit_15.toPlainText()
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        branch=branchs[-1][0]
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        
        self.cur.execute('''SELECT date , time_out FROM employee_absence where date=%s AND name=%s''',(date,name))
        leaving=self.cur.fetchall()
        #print (leaving[-1])
        if leaving==():
            self.cur.execute('''
            INSERT INTO employee_absence(name,branch,date, time_in, comment)
            VALUES(%s,%s,%s,%s,%s)''',(name,branch,date,time,comment))
            self.db.commit()
            self.textEdit_15.setText('')
            QMessageBox.about(self,'hint','done')
            
        elif leaving[-1][1]!= None:
            self.cur.execute('''
            INSERT INTO employee_absence(name,branch,date, time_in, comment)
            VALUES(%s,%s,%s,%s,%s)''',(name,branch,date,time,comment))
            self.db.commit()
            self.textEdit_15.setText('')
            QMessageBox.about(self,'hint','done')
        else:
            QMessageBox.about(self,'hint','this employee already came')
        
       
            
#####################################

#####################################sales tab

    def sell_showclient(self):#show client money balance
        name=self.lineEdit_17.text()

        if name=='':
            QMessageBox.about(self, 'caution', 'inter client name')
        else:
            self.cur.execute(''' SELECT name FROM clients
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self, 'caution', 'cant find client')
            else:
                qin=0
                qout=0
                self.cur.execute('''select amount FROM client_balance
                WHERE name=%s AND move=%s''',(name,'in'))
                allin=self.cur.fetchall()
                for i in allin:
                    qin+=float(i[0])
                self.cur.execute('''select amount FROM client_balance
                WHERE name=%s AND move=%s''',(name,'out'))
                allout=self.cur.fetchall()
                for i in allout:
                    qout+=float(i[0])
                balance=qout-qin
                self.lineEdit_18.setText(str(balance))
                self.lineEdit_17.setEnabled(False)

#########################################
    def sell_remove_client(self):
        self.lineEdit_18.setText('')
        self.lineEdit_17.setEnabled(True)
        self.lineEdit_17.setText('')


##########################################
    def sell_search(self):
        barcode=self.lineEdit_38.text()
        name=self.lineEdit_39.text()
        self.cur.execute('''SELECT branch FROM default_branch''')
        branchs=self.cur.fetchall()
        branch=branchs[-1][0]
        fast_code=self.lineEdit_78.text()
        expiry=self.comboBox_23.currentText()

        if name=='' and barcode == '' and fast_code=='' :
            QMessageBox.about(self,'caution','inter name or barcode or fast code')

        elif name=='' and fast_code=='' and barcode!='':
            self.cur.execute('''SELECT name, price, quantity,expiry FROM item_quant
            WHERE special_code=%s''',(barcode))
            qdata=self.cur.fetchall()
            if qdata==():
                self.cur.execute('''SELECT name, sell_price, req_quan,fast_code,have_expiry FROM items
                WHERE barcode=%s''',(barcode))
                data=self.cur.fetchall()
                if data==():
                    QMessageBox.about(self,'caution','item not found')
                else:
                    name=data[0][0]
                    self.lineEdit_39.setText(name)#name field
                    self.lineEdit_78.setText(str(data[0][3]))#fast code field
                    self.lineEdit_81.setText(str(data[0][1]))#sell price field
                    self.lineEdit_84.setText(str(data[0][2]))#request quantity field
                    
                
            else:
                self.cur.execute('''SELECT name, sell_price, req_quan,fast_code,have_expiry FROM items
                WHERE name=%s''',(qdata[0][0]))
                data=self.cur.fetchall()
            
                if data==():
                    QMessageBox.about(self,'caution','item not found')
                else:
                    name=data[0][0]
                    self.lineEdit_39.setText(name)#name field
                    self.lineEdit_78.setText(str(data[0][3]))#fast code field
                    self.lineEdit_81.setText(str(qdata[0][1]))#sell price field
                    self.lineEdit_84.setText(str(data[0][2]))#request quantity field
                    self.lineEdit_40.setText(str(qdata[0][2]))#quantity field
                    self.comboBox_23.addItem(str(qdata[0][3]))#expiry field
                    

        elif name!='' and barcode==''or  fast_code=='':
            self.cur.execute('''SELECT barcode, sell_price, req_quan,fast_code,have_expiry FROM items
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found')
            else:
                self.lineEdit_38.setText(data[0][0])
                name=self.lineEdit_39.text()
                self.lineEdit_78.setText(str(data[0][3]))
                self.lineEdit_81.setText(str(data[0][1]))
                self.lineEdit_84.setText(str(data[0][2]))

        elif name=='' or barcode=='' and fast_code!='':
            self.cur.execute('''SELECT barcode,name, sell_price, req_quan,have_expiry FROM items
            WHERE fast_code=%s''',(fast_code))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found')
            else:
                name=data[0][1]
                self.lineEdit_39.setText(name)
                self.lineEdit_38.setText(data[0][0])
                self.lineEdit_81.setText(str(data[0][1]))
                self.lineEdit_84.setText(str(data[0][2]))

        elif name!='' and barcode != '' and fast_code!='' :
                self.cur.execute('''SELECT name, sell_price, req_quan,fast_code,have_expiry FROM items
                WHERE barcode=%s''',(barcode))
                data=self.cur.fetchall()
                if data==():
                    QMessageBox.about(self,'caution','item not found')
                else:
                    name=data[0][0]
                    self.lineEdit_39.setText(name)
                    self.lineEdit_78.setText(str(data[0][3]))
                    self.lineEdit_81.setText(str(data[0][1]))
                    self.lineEdit_84.setText(str(data[0][2]))

        if data !=() and qdata==():
            if data[0][4]=='1':

                self.cur.execute('''SELECT quantity ,price,expiry FROM item_quant
                    WHERE name=%s AND store=%s''',(name, branch))
                quants=self.cur.fetchall()
                if quants==():
                    QMessageBox.about(self,'caution','not enough balance')
                else:
                    self.comboBox_23.clear()
                    for i in quants:
                        self.comboBox_23.addItem(str(i[2]))
                    self.lineEdit_41.setText(str(quants[0][0]))
                    if quants[0][0]==0:
                        QMessageBox.about(self,'caution','not enough balance')
    
                    elif quants[0][0]<=data[0][2]:
    
                        self.lineEdit_84.setStyleSheet('background-color: rgb(255, 124, 166);')
                        self.lineEdit_41.setStyleSheet('background-color: rgb(255, 124, 166);')
    
                    self.pushButton_50.setEnabled(True)
            
            else:
                
                self.cur.execute('''SELECT quantity ,price,special_code FROM item_quant
                    WHERE name=%s AND store=%s''',(name, branch))
                quants=self.cur.fetchall()
                if quants==():
                    QMessageBox.about(self,'caution','not enough balance')
                else:
                    for i in quants:
                        self.comboBox_23.addItem(i[2])
                    self.lineEdit_41.setText(str(quants[0][0]))
                    if quants[0][0]==0:
                        QMessageBox.about(self,'caution','not enough balance')
    
                    elif quants[0][0]<=data[0][2]:
    
                        self.lineEdit_84.setStyleSheet('background-color: rgb(255, 124, 166);')
                        self.lineEdit_41.setStyleSheet('background-color: rgb(255, 124, 166);')
    
                    self.pushButton_50.setEnabled(True)
                
                

        else:
            pass

#####################################################
    def sell_additem(self):#add item to the bill
        #################################variables
        name=self.lineEdit_39.text()
        amount=self.lineEdit_40.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        price=self.lineEdit_81.text()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        store=branchs[-1][0]
        balance=self.lineEdit_41.text()

        if self.lineEdit_17.text()=='':
            cl_vend='cash'
        else:
            cl_vend=self.lineEdit_17.text()
        total_bill=0
        bill_id=self.lineEdit_37.text()
        ########################################

        if amount=='':
            QMessageBox.about(self,'caution','inter desired amount')
            self.lineEdit_40.setFocus()
        elif not isfloat(amount) or not isfloat(price):
            QMessageBox.about(self,'caution','inter price amount numbers only')
        else:
            total=(int(amount)*float(price))
            self.lineEdit_83.setText(str(total))
            if float(amount)>float(balance):############add items to temp bill
                QMessageBox.about(self,'caution','balance is not enough')

            else:
                self.cur.execute('''
                        INSERT INTO temp_bill(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,move)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                        ''',(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,'sell'))
                self.db.commit()

                self.cur.execute('''SELECT id,name,amount,price,total,move
                                FROM temp_bill WHERE move=%s''',('sell'))

                while self.tableWidget_3.rowCount()>0:
                    self.tableWidget_3.removeRow(0)

                datas=self.cur.fetchall()
                for row , data in enumerate(datas):
                    total_bill+=float(data[4])
                    self.lineEdit_43.setText(str(total_bill))
                    self.tableWidget_3.insertRow(row)
                    for col, item in enumerate(data):
                        self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(item)))


                self.pushButton_50.setEnabled(False)
                self.pushButton_51.setEnabled(True)


                self.lineEdit_38.setText('')
                self.lineEdit_38.setFocus()
                self.lineEdit_78.setText('')
                self.lineEdit_39.setText('')
                self.lineEdit_40.setText('')
                self.lineEdit_81.setText('')
                self.lineEdit_83.setText('')
                self.lineEdit_41.setText('')
                self.lineEdit_84.setText('')

###############################################

    def sell_removeitem(self):
        total_bill=0
        item_id=self.lineEdit_79.text()
        self.cur.execute('''SELECT id, total FROM temp_bill WHERE id=%s AND move=%s''',(item_id,'sell'))
        check=self.cur.fetchall()

        if item_id=='':
            QMessageBox.about(self,'caution','inter ID first')
            self.lineEdit_79.setFocus()
        elif check==():
            QMessageBox.about(self,'caution','inter correct ID')
            self.lineEdit_79.setFocus()
        else:
            total=check[0][1]
            self.cur.execute('''DELETE FROM temp_bill WHERE id=%s AND move = %s''',(item_id,'sell'))
            self.db.commit()
            while self.tableWidget_3.rowCount()>0:
                    self.tableWidget_3.removeRow(0)
            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('sell'))
            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                self.tableWidget_3.insertRow(row)
                total_bill+=float(data[4])
                self.lineEdit_43.setText(str(total_bill))
                for col, item in enumerate(data):
                    self.tableWidget_3.setItem(row,col,QTableWidgetItem(str(item)))
            self.lineEdit_79.setText('')
        self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('sell'))
        check=self.cur.fetchall()
        if check==():
            self.pushButton_51.setEnabled(False)
            self.lineEdit_43.setText('0')

#################################################
    def sell_sell(self):#save the bill
        if self.lineEdit_37.text()=='':
            self.show_returnsales()
        comment=self.lineEdit_104.text()
        bill_total=self.lineEdit_43.text()
        paid=self.lineEdit_42.text()
        cl_vend=self.lineEdit_17.text()
        ###########################move to main table
        if self.lineEdit_42.text()=='':
            QMessageBox.about(self,'caution', 'inter money paid')
            self.lineEdit_42.setFocus()
        elif not isfloat(self.lineEdit_42.text()):
            QMessageBox.about(self,'caution', 'inter only numbers')
            self.lineEdit_42.setFocus()
        elif cl_vend=='' and float(paid)!=float(bill_total):
            QMessageBox.about(self,'caution', 'inter all the money')  
            self.lineEdit_42.setFocus()                      
        else:
            self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('sell'))
            bill_items=self.cur.fetchall()
            for item in bill_items:
                name=item[1]
                amount=item[2]
                date=item[3]
                time=item[4]
                price=item[5]
                employee=item[6]
                store=item[7]
                total=item[8]
                bill_id=item[9]
                cl_vend=item[10]
                self.cur.execute('''INSERT INTO items_sell(name,amount,date,
                time,price,employee,store,total,bill_id,client,comment)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (name,amount,date,time,price,employee,store,total,bill_id,cl_vend,comment))
                self.db.commit()
            ##################################fill quantity table
                self.cur.execute('''SELECT name, quantity FROM item_quant
                WHERE name=%s AND store=%s''',(name,store))
                check=self.cur.fetchall()
                if check==():
                    self.cur.execute('''
                    INSERT INTO item_quant(name,quantity,store)
                    VALUES(%s,%s,%s)
                    ''',(name,amount,store))
                    self.db.commit()
                elif check != ():
                    quantity=float(check[0][1])-float(amount)
                    self.cur.execute('''UPDATE item_quant SET quantity=%s
                     WHERE name=%s AND store=%s
                ''',(quantity,name,store))
                self.db.commit()

                #######################empty table widget

            ########################################fill bill table
            number=bill_items[0][9]
            date=bill_items[0][3]
            time=bill_items[0][4]
            employee=bill_items[0][6]
            store=bill_items[0][7]
            cl_vend=bill_items[0][10]
            self.cur.execute(''' INSERT INTO bill_no(number,date,time,
            employee,store,move,cl_vend,bill_total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (number,date,time,employee,store,'sell',cl_vend,bill_total))
#################################################fill safe drawer 
            
            if cl_vend=='':
                cl_vend='cash'
                if  float(self.lineEdit_42.text())!= float(self.lineEdit_43.text()):
                    QMessageBox.about(self,'caution','inter iqual money')
                else:
                    self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'sell',amount,date,time,comment,employee,'in',cl_vend))
                    self.empty_sell()
                    self.show_sales()


            else:
                amount=float(self.lineEdit_43.text())-float(self.lineEdit_42.text())
                self.cur.execute('''INSERT INTO client_balance(name,
                amount,date,time,move,reason,employee,branch,bill_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',(cl_vend,amount,date,time,'out','sell',employee,store,bill_id))
                amount=self.lineEdit_42.text()
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,date,time,comment,employee,move,source)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'sell',amount,date,time,comment,employee,'in',cl_vend))

                self.empty_sell()
                self.show_sales()
###################################

    def return_sell_showclient(self):#show client money balance
        name=self.lineEdit_57.text()

        if name=='':
            QMessageBox.about(self, 'caution', 'inter client name')
        else:
            self.cur.execute(''' SELECT name FROM clients
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self, 'caution', 'cant find client')
            else:
                qin=0
                qout=0
                self.cur.execute('''select amount FROM client_balance
                WHERE name=%s AND move=%s''',(name,'in'))
                allin=self.cur.fetchall()
                for i in allin:
                    qin+=float(i[0])
                self.cur.execute('''select amount FROM client_balance
                WHERE name=%s AND move=%s''',(name,'out'))
                allout=self.cur.fetchall()
                for i in allout:
                    qout+=float(i[0])
                balance=qout-qin
                self.lineEdit_80.setText(str(balance))
                self.lineEdit_57.setEnabled(False)
##########################################
    def return_sell_removeclient(self):
        self.lineEdit_80.setText('')
        self.lineEdit_57.setEnabled(True)
        self.lineEdit_57.setText('')
##########################################

    def return_sell_search(self):
        barcode=self.lineEdit_45.text()
        name=self.lineEdit_46.text()
        self.cur.execute('''SELECT branch FROM default_branch''')
        branchs=self.cur.fetchall()
        branch=branchs[-1][0]
        fast_code=self.lineEdit_89.text()

        if name=='' and barcode == '' and fast_code=='' :
            QMessageBox.about(self,'caution','inter name or barcode or fast code')

        elif name=='' and fast_code=='' and barcode!='':
            self.cur.execute('''SELECT name, sell_price, req_quan,fast_code FROM items
            WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found1')
            else:
                name=data[0][0]
                self.lineEdit_46.setText(name)
                self.lineEdit_89.setText(str(data[0][3]))
                self.lineEdit_82.setText(str(data[0][1]))
                self.lineEdit_88.setText(str(data[0][2]))

                self.cur.execute('''SELECT * FROM items_sell WHERE name=%s''',(name))
                x=self.cur.fetchall()
                if x==():
                    QMessageBox.about(self,'caution','item did not sold before')
                else:
                    self.lineEdit_46.setText(name)
                    self.lineEdit_89.setText(str(data[0][3]))
        elif name!='' and barcode==''or  fast_code=='':
            self.cur.execute('''SELECT barcode, sell_price, req_quan,fast_code FROM items
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found2')
            else:
                self.lineEdit_45.setText(data[0][0])
                name=self.lineEdit_46.text()
                self.lineEdit_89.setText(str(data[0][3]))
                self.lineEdit_82.setText(str(data[0][1]))
                self.lineEdit_88.setText(str(data[0][2]))

                self.cur.execute('''SELECT * FROM items_sell WHERE name=%s''',(name))
                x=self.cur.fetchall()
                if x==():
                    QMessageBox.about(self,'caution','item did not sold before')
                else:
                    self.lineEdit_89.setText(str(data[0][3]))
        elif name=='' or barcode=='' and fast_code!='':
            self.cur.execute('''SELECT barcode,name, sell_price, req_quan FROM items
            WHERE fast_code=%s''',(fast_code))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found3')
            else:
                self.lineEdit_45.setText(data[0][0])
                name=data[0][1]
                self.lineEdit_46.setText(str(data[0][1]))
                self.lineEdit_82.setText(str(data[0][2]))
                self.lineEdit_88.setText(str(data[0][3]))
                self.cur.execute('''SELECT * FROM items_sell WHERE name=%s''',(name))
                x=self.cur.fetchall()
                if x==():
                    QMessageBox.about(self,'caution','item did not sold before')
                else:
                    self.lineEdit_46.setText(name)

                    self.lineEdit_45.setText(data[0][0])


        elif name!='' and barcode != '' and fast_code!='' :
            self.cur.execute('''SELECT name, sell_price, req_quan,fast_code FROM items
            WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found4')
            else:
                name=data[0][0]
                self.lineEdit_46.setText(name)
                self.lineEdit_89.setText(str(data[0][3]))
                self.lineEdit_82.setText(str(data[0][1]))
                self.lineEdit_88.setText(str(data[0][2]))

                self.cur.execute('''SELECT * FROM items_sell WHERE name=%s''',(name))
                x=self.cur.fetchall()
                if x==():
                    QMessageBox.about(self,'caution','item did not sold before')
                else:
                    self.lineEdit_46.setText(name)
                    self.lineEdit_89.setText(str(data[0][3]))
                    self.lineEdit_82.setText(str(data[0][1]))
                    self.lineEdit_88.setText(str(data[0][2]))
        else:
            QMessageBox.about(self,'caution','search with different data')
        if data!=():

            self.cur.execute('''SELECT quantity FROM item_quant
                WHERE name=%s AND store=%s''',(name, branch))
            quants=self.cur.fetchall()
            if quants!=():
                self.lineEdit_49.setText(str(quants[0][0]))
                self.pushButton_52.setEnabled(True)


        else:

            pass

   ###################################################
    def return_sell_additem(self):#add item to the bill
        name=self.lineEdit_46.text()
        amount=self.lineEdit_48.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        price=self.lineEdit_82.text()
        total_bill=0
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        store=branchs[-1][0]
        balance=self.lineEdit_49.text()

        # self.cur.execute('''SELECT number FROM bill_no''')
        # numbers=self.cur.fetchall()
        bill_id=self.lineEdit_91.text()#int(numbers[-1][0])+1
       # print(bill_id)
        #self.lineEdit_91.setText(str(bill_id))
        if self.lineEdit_57.text()=='':
            cl_vend='cash'
        else:
            cl_vend=self.lineEdit_57.text()
        ########################################

        if amount=='':
            QMessageBox.about(self,'caution','inter desired amount')
            self.lineEdit_48.setFocus()
        elif not isfloat(amount) or not isfloat(price):
            QMessageBox.about(self,'caution','inter price & amount in numbers')
        else:
            total=(int(amount)*float(price))
            self.lineEdit_87.setText(str(total))

            self.cur.execute('''
                    INSERT INTO temp_bill(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,move)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,'rsell'))
            self.db.commit()

            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('rsell'))

            while self.tableWidget_4.rowCount()>0:
                self.tableWidget_4.removeRow(0)

            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                self.tableWidget_4.insertRow(row)
                total_bill+=float(data[4])
                self.lineEdit_51.setText(str(total_bill))
                for col, item in enumerate(data):
                    self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))

            self.pushButton_52.setEnabled(False)
            self.pushButton_53.setEnabled(True)

            self.lineEdit_45.setText('')
            self.lineEdit_89.setText('')
            self.lineEdit_46.setText('')
            self.lineEdit_48.setText('')
            self.lineEdit_82.setText('')
            self.lineEdit_87.setText('')
            self.lineEdit_49.setText('')
            self.lineEdit_88.setText('')
            self.lineEdit_45.setFocus()
#############################################################
    def returnsell_removeitem(self):
        item_id=self.lineEdit_90.text()
        total_bill=0
        self.cur.execute('''SELECT id, total FROM temp_bill WHERE id=%s AND move=%s''',(item_id,'rsell'))
        check=self.cur.fetchall()

        if item_id=='':
            QMessageBox.about(self,'caution','inter ID first')
            self.lineEdit_90.setFocus()
        elif check==():
            QMessageBox.about(self,'caution','inter correct ID')
            self.lineEdit_90.setFocus()
        else:
            total=check[0][1]
            self.cur.execute('''DELETE FROM temp_bill WHERE id=%s AND move=%s''',(item_id, 'rsell'))
            self.db.commit()
            while self.tableWidget_4.rowCount()>0:
                    self.tableWidget_4.removeRow(0)
            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('rsell'))
            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                total_bill+=float(data[4])
                self.lineEdit_51.setText(str(total_bill))
                self.tableWidget_4.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_4.setItem(row,col,QTableWidgetItem(str(item)))
            self.lineEdit_90.setText('')
        self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('rsell'))
        check=self.cur.fetchall()
        if check==():
            self.pushButton_53.setEnabled(False)
            self.lineEdit_51.setText('0')
###################################################
    def returnsell_return(self):#save the bill
        if self.lineEdit_91.text()=='':
            self.show_returnsales()
        comment=self.lineEdit_105.text()
        bill_total=self.lineEdit_51.text()
        paid=self.lineEdit_50.text()
        cl_vend=self.lineEdit_57.text()
        ###########################move to main table
        if self.lineEdit_50.text()=='':
            QMessageBox.about(self,'caution', 'inter money paid')
            self.lineEdit_50.setFocus()
        elif not isfloat(self.lineEdit_50.text()):
            QMessageBox.about(self,'caution', 'inter only numbers')
            self.lineEdit_50.setFocus()
        elif cl_vend=='' and float(paid)!=float(bill_total):
            QMessageBox.about(self,'caution', 'inter all the money')
            self.lineEdit_50.setFocus()
        else:
            self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('rsell'))
            bill_items=self.cur.fetchall()
            for item in bill_items:
                name=item[1]
                amount=item[2]
                date=item[3]
                time=item[4]
                price=item[5]
                employee=item[6]
                store=item[7]
                total=item[8]
                bill_id=item[9]
                cl_vend=item[10]
                self.cur.execute('''INSERT INTO items_sell_ret(name,amount,date,
                time,price,employee,store,total,bill_id,client,comment)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (name,amount,date,time,price,employee,store,total,bill_id,cl_vend,comment))
                self.db.commit()
            ##################################fill quantity table
                self.cur.execute('''SELECT name, quantity FROM item_quant
                WHERE name=%s AND store=%s''',(name,store))
                check=self.cur.fetchall()
                if check==():
                    self.cur.execute('''
                    INSERT INTO item_quant(name,quantity,store)
                    VALUES(%s,%s,%s)
                    ''',(name,amount,store))
                    self.db.commit()
                elif check != ():
                    quantity=float(check[0][1])+float(amount)
                    self.cur.execute('''UPDATE item_quant SET quantity=%s
                     WHERE name=%s AND store=%s
                ''',(quantity,name,store))
                self.db.commit()

                #######################empty table widget

            ########################################fill bill table
            number=bill_items[0][9]
            date=bill_items[0][3]
            time=bill_items[0][4]
            employee=bill_items[0][6]
            store=bill_items[0][7]
            move='rsell'
            cl_vend=bill_items[0][10]
            self.cur.execute(''' INSERT INTO bill_no(number,date,time,
            employee,store,move,cl_vend,bill_total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (number,date,time,employee,store,move,cl_vend,bill_total))
#########################################################fill drawer and safe
            amount=self.lineEdit_50.text()
            cl_vend=self.lineEdit_57.text()
            if cl_vend=='':
                cl_vend='cash'
               
                if float(self.lineEdit_51.text())!= float(self.lineEdit_50.text()):
                    QMessageBox.about(self,'caution','this is cash bill')
                else:
                    if self.comboBox_2.currentText()=='DRAWER':
                        if float(self.lineEdit_106.text())>= float(self.lineEdit_51.text()):

                            self.cur.execute('''INSERT INTO drawer_moves(branch,
                            reason,amount,date,time,comment,employee,move,source)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'rsell',
                            amount,date,time,comment,employee,'out',cl_vend))
                            self.empty_returnsell()
                            self.show_returnsales()
                        else:
                            QMessageBox.about(self,'caution','no enough balance in the drawer')
                    elif self.comboBox_2.currentText()=='SAFE':
                        if float(self.lineEdit_106.text())>= float(self.lineEdit_51.text()):
                            self.cur.execute('''INSERT INTO safe_moves(branch,
                            reason,amount,date,time,comment,employee,move,source)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'rsell',
                            amount,date,time,comment,employee,'out',cl_vend))
                            self.empty_returnsell()
                            self.show_returnsales()
                        else:
                            QMessageBox.about(self,'caution','no enough balance in the safe')

            else:
                amount=float(self.lineEdit_51.text())-float(self.lineEdit_50.text())
                
                self.cur.execute('''INSERT INTO client_balance(name,
                amount,date,time,move,reason,employee,branch,bill_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                ''',(cl_vend,amount,date,time,'in','rsell',employee,store,bill_id))
                amount=self.lineEdit_50.text()
                if self.comboBox_2.currentText()=='DRAWER':
                    if float(self.lineEdit_106.text())>= float(self.lineEdit_51.text()):
                        self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,
                        date,time,comment,employee,move,source)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (store,'rsell',amount,date,time,comment,employee,'out',cl_vend))
                        self.empty_returnsell()
                        self.show_returnsales()
                    else:
                        QMessageBox.about(self,'caution','no enough balance in the safe')

                if self.comboBox_2.currentText()=='SAFE':
                    if float(self.lineEdit_106.text())>= float(self.lineEdit_51.text()):
                        self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,
                        date,time,comment,employee,move,source)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (store,'rsell',amount,date,time,comment,employee,'out',cl_vend))
                        self.empty_returnsell()
                        self.show_returnsales()
                    else:
                        QMessageBox.about(self,'caution','no enough balance in the safe')
        

#####################################


#####################################purchase tab

    def purchase_showvendor(self):#show vendor money balance
        name=self.lineEdit_69.text()

        if name=='':
            QMessageBox.about(self, 'caution', 'inter vendor name')
        else:
            self.cur.execute(''' SELECT name FROM vendors
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self, 'caution', 'cant find vendor')
            else:
                qin=0
                qout=0
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'in'))
                allin=self.cur.fetchall()
                for i in allin:
                    qin+=float(i[0])
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'out'))
                allout=self.cur.fetchall()
                for i in allout:
                    qout+=float(i[0])
                balance=qout-qin
                self.lineEdit_70.setText(str(balance))
                self.lineEdit_69.setEnabled(False)
##########################################
    def purchase_removevendor(self):
        self.lineEdit_70.setText('')
        self.lineEdit_69.setEnabled(True)
        self.lineEdit_69.setText('')
##############################################
    def purchase_search(self):

        barcode=self.lineEdit_47.text()
        name=self.lineEdit_63.text()
        self.cur.execute('''SELECT branch FROM default_branch''')
        branchs=self.cur.fetchall()
        branch=branchs[-1][0]
        fast_code=self.lineEdit_93.text()

        if name=='' and barcode == '' and fast_code=='' :
            QMessageBox.about(self,'caution','inter name or barcode or fast code')

        elif name=='' and fast_code=='' and barcode!='':

            self.cur.execute('''SELECT name, pur_price, req_quan,fast_code,have_expiry,sell_price FROM items
            WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found1')
            else:
                name=data[0][0]
                self.lineEdit_63.setText(name)
                self.lineEdit_93.setText(str(data[0][3]))
                self.lineEdit_119.setText(str(data[0][1]))
                self.lineEdit_92.setText(str(data[0][2]))
                self.lineEdit_85.setText(str(data[0][5]))

        elif name!='' and barcode==''or  fast_code=='':
            self.cur.execute('''SELECT barcode, pur_price, req_quan,fast_code,have_expiry,sell_price FROM items
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found2')
            else:
                self.lineEdit_47.setText(data[0][0])
                name=self.lineEdit_63.text()
                self.lineEdit_93.setText(str(data[0][3]))
                self.lineEdit_85.setText(str(data[0][5]))
                self.lineEdit_119.setText(str(data[0][1]))
                self.lineEdit_92.setText(str(data[0][2]))

        elif name=='' or barcode=='' and fast_code!='':
            self.cur.execute('''SELECT barcode,name, pur_price, req_quan,have_expiry,sell_price FROM items
            WHERE fast_code=%s''',(fast_code))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found3')
            else:
                name=data[0][1]
                self.lineEdit_63.setText(name)
                self.lineEdit_47.setText(data[0][0])
                self.lineEdit_119.setText(str(data[0][2]))
                self.lineEdit_92.setText(str(data[0][3]))
                self.lineEdit_85.setText(str(data[0][5]))
        #if data!=():
        elif name!='' and barcode != '' and fast_code!='' :
            self.cur.execute('''SELECT name, pur_price, req_quan,fast_code,have_expiry,sell_price FROM items
            WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found1')
            else:
                name=data[0][0]
                self.lineEdit_63.setText(name)
                self.lineEdit_93.setText(str(data[0][3]))
                self.lineEdit_119.setText(str(data[0][1]))
                self.lineEdit_92.setText(str(data[0][2]))
                self.lineEdit_85.setText(str(data[0][5]))
        else:
            QMessageBox.about(self,'caution','search with different data')
        
            
        if data !=():
            if data[0][4]=='0':
                self.dateEdit_36.setEnabled(False)
            else:
                self.dateEdit_36.setEnabled(True)

            name=self.lineEdit_63.text()
            self.cur.execute('''SELECT SUM(quantity) FROM item_quant
                WHERE name=%s AND store=%s''',(name, branch))
            quants=self.cur.fetchall()
            print (quants)
            if quants==() or quants[0][0] == None:
                self.lineEdit_65.setText('0')
                self.pushButton_56.setEnabled(True)
            else:
                self.lineEdit_65.setText(str(quants[0][0]))
                self.pushButton_56.setEnabled(True)

            if float(self.lineEdit_65.text())<=float(self.lineEdit_92.text()):

                self.lineEdit_65.setStyleSheet('background-color: rgb(255, 124, 166);')
                self.lineEdit_92.setStyleSheet('background-color: rgb(255, 124, 166);')

            else:
                pass

        else:
            pass
################################################################
    def purchase_additem(self):#add item to the bill
        name=self.lineEdit_63.text()
        amount=self.lineEdit_64.text()
        date=datetime.date.today()
        edate=self.dateEdit_36.date().toPyDate().strftime("%Y%m%d")
        time=datetime.datetime.now().strftime('%H:%M')
        price=self.lineEdit_85.text()
        cost=self.lineEdit_119.text()
        expiry=self.dateEdit_36.date().toPyDate()
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        store=branchs[-1][0]
        balance=self.lineEdit_65.text()

        bill_id=self.lineEdit_71.text()#int(numbers[-1][0])+1
        
        if self.lineEdit_69.text()=='':
            cl_vend='cash'
        else:
            cl_vend=self.lineEdit_69.text()
        total_bill=0
        self.cur.execute('''SELECT id FROM items WHERE name=%s''',(name))
        code=self.cur.fetchall()
        special_code=str(code[0][0])+str(date.strftime("%Y%m%d"))+str(bill_id)
        ########################################
        
        if amount=='':
            QMessageBox.about(self,'caution','inter desired amount')
            self.lineEdit_64.setFocus()
        elif not isfloat(amount) or not isfloat(price):
            QMessageBox.about(self,'caution','inter price amount numbers only')
        else:
            total=(float(amount)*float(cost))
            self.lineEdit_86.setText(str(total))

            self.cur.execute('''INSERT INTO temp_bill(name,special_code,amount,
            date,time,price,employee,expiry,store,total,bill_id,cl_vend,move,cost)
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
            (name,special_code,amount,date,time,price,employee,expiry,store,total,bill_id,cl_vend,'pur',cost))
            self.db.commit()

            self.cur.execute('''SELECT id,name,amount,cost,total,move,price
                            FROM temp_bill WHERE move=%s''',('pur'))

            while self.tableWidget_5.rowCount()>0:
                self.tableWidget_5.removeRow(0)

            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                total_bill+=float(data[4])
                self.lineEdit_67.setText(str(total_bill))
                self.tableWidget_5.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_5.setItem(row,col,QTableWidgetItem(str(item)))


                self.pushButton_56.setEnabled(False)
                self.pushButton_58.setEnabled(True)


                self.lineEdit_47.setText('')
                self.lineEdit_47.setFocus()
                self.lineEdit_93.setText('')
                self.lineEdit_63.setText('')
                self.lineEdit_64.setText('')
                self.lineEdit_85.setText('')
                self.lineEdit_86.setText('')
                self.lineEdit_65.setText('')
                self.lineEdit_92.setText('')

#############################################################
    def purchase_removeitem(self):
        total_bill=0
        item_id=self.lineEdit_94.text()
        self.cur.execute('''SELECT id, total FROM temp_bill WHERE id=%s AND move=%s''',(item_id,'pur'))
        check=self.cur.fetchall()

        if item_id=='':
            QMessageBox.about(self,'caution','inter ID first')
            self.lineEdit_94.setFocus()
        elif check==():
            QMessageBox.about(self,'caution','inter correct ID')
            self.lineEdit_94.setFocus()
        else:
            total=check[0][1]
            self.cur.execute('''DELETE FROM temp_bill WHERE id=%s AND move = %s''',(item_id,'pur'))
            self.db.commit()
            while self.tableWidget_5.rowCount()>0:
                    self.tableWidget_5.removeRow(0)
            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('pur'))
            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                self.tableWidget_5.insertRow(row)
                total_bill+=float(data[4])
                self.lineEdit_67.setText(str(total_bill))
                for col, item in enumerate(data):
                    self.tableWidget_5.setItem(row,col,QTableWidgetItem(str(item)))
            self.lineEdit_94.setText('')
        self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('pur'))
        check=self.cur.fetchall()
        if check==():
            self.pushButton_58.setEnabled(False)
            self.lineEdit_67.setText('0')
##############################################################
    def purchase_purchase(self):#save the bill
        if self.lineEdit_71.text()=='':
            self.show_returnsales()
        comment=self.lineEdit_108.text()
        bill_total=self.lineEdit_67.text()
        cl_vend=self.lineEdit_69.text()
        paid=self.lineEdit_66.text()
        
        ###########################move to main table
        if self.lineEdit_66.text()=='':
            QMessageBox.about(self,'caution', 'inter money paid')
            self.lineEdit_66.setFocus()
        elif not isfloat(self.lineEdit_66.text()):
            QMessageBox.about(self,'caution', 'inter only numbers')
            self.lineEdit_66.setFocus()
        elif cl_vend=='' and float(bill_total)!=float(paid):
            QMessageBox.about(self,'caution','you must pay all the money')
            self.lineEdit_66.setFocus()
        else:
            self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('pur'))
            bill_items=self.cur.fetchall()
            for item in bill_items:
                print(item[4])
                name=item[1]
                special_code=item[2]
                amount=item[3]
                date=item[4]
                time=item[5]
                price=item[6]
                employee=item[7]
                expiry=item[8]
                store=item[9]
                total=item[10]
                bill_id=item[11]
                cl_vend=item[12]
                self.cur.execute('''INSERT INTO items_pur(name,special_code,amount,date,
                time,price,employee,expiry,store,total,bill_id,vendor,comment)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (name,special_code,amount,date,time,price,employee,expiry,store,total,bill_id,cl_vend,comment))
                self.db.commit()
            ##################################fill quantity table
                
            
                self.cur.execute('''
                INSERT INTO item_quant(name,special_code,quantity,expiry,store)
                VALUES(%s,%s,%s,%s,%s)
                ''',(name,item[2],amount,item[8],store))
                self.db.commit()
           

            ########################################fill bill table
            number=bill_items[0][11]
            date=bill_items[0][4]
            time=bill_items[0][5]
            employee=bill_items[0][7]
            store=bill_items[0][9]
            cl_vend=bill_items[0][12]
            self.cur.execute(''' INSERT INTO bill_no(number,date,time,
            employee,store,move,cl_vend,bill_total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (number,date,time,employee,store,'pur',cl_vend,bill_total))
###################################################fill safe drawer moves
            amount=self.lineEdit_66.text()
            cl_vend=self.lineEdit_69.text()
            if cl_vend=='':
                cl_vend='cash'
                if float(self.lineEdit_66.text())!=float(self.lineEdit_67.text()):
                    QMessageBox.about(self,'caution','you must pay all the money')
                else:

                    if self.comboBox_4.currentText()=='DRAWER':
                        if float(self.lineEdit_107.text())>= float(self.lineEdit_67.text()):

                            self.cur.execute('''INSERT INTO drawer_moves(branch,
                            reason,amount,date,time,comment,employee,move,source)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'pur',
                            amount,date,time,comment,employee,'out',cl_vend))
                            self.empty_purchase()
                            self.show_purchase()
                        else:
                            QMessageBox.about(self,'caution','no enough balance in the drawer')
                    elif self.comboBox_4.currentText()=='SAFE':
                        if float(self.lineEdit_107.text())>= float(self.lineEdit_67.text()):
                            self.cur.execute('''INSERT INTO safe_moves(branch,
                            reason,amount,date,time,comment,employee,move,source)
                            VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'pur',
                            amount,date,time,comment,employee,'out',cl_vend))
                            self.empty_purchase()
                            self.show_purchase()
                        else:
                            QMessageBox.about(self,'caution','no enough balance in the safe')

            else:
                if float(self.lineEdit_107.text())>= float(self.lineEdit_66.text()):
                    amount=float(self.lineEdit_67.text())-float(self.lineEdit_66.text())
                    self.cur.execute('''INSERT INTO vendor_balance(name,
                    amount,date,time,move,reason,employee,branch,bill_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',(cl_vend,amount,date,time,'out','pur',employee,store,bill_id))
                    amount=self.lineEdit_66.text()
                    if self.comboBox_4.currentText()=='DRAWER':
                        
                        self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,
                        date,time,comment,employee,move,source)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (store,'pur',amount,date,time,comment,employee,'out',cl_vend))
                        self.empty_purchase()
                        self.show_purchase()
                    
                    elif self.comboBox_4.currentText()=='SAFE':
                        self.cur.execute('''INSERT INTO safe_moves(branch,reason,amount,
                        date,time,comment,employee,move,source)
                        VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                        (store,'pur',amount,date,time,comment,employee,'out',cl_vend))
                        self.empty_purchase()
                        self.show_purchase()
                else:
                        QMessageBox.about(self,'caution','no enough balance in the drawer')    
            
                

##############################################################
    def return_purchase_showvendor(self):#show vendor money balance

        name=self.lineEdit_97.text()
        if name=='':
            QMessageBox.about(self, 'caution', 'inter vendor name')
        else:
            self.cur.execute(''' SELECT name FROM vendors
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self, 'caution', 'cant find vendor')
            else:
                qin=0
                qout=0
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'in'))
                allin=self.cur.fetchall()
                for i in allin:
                    qin+=float(i[0])
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'out'))
                allout=self.cur.fetchall()
                for i in allout:
                    qout+=float(i[0])
                balance=qout-qin
                self.lineEdit_98.setText(str(balance))
                self.lineEdit_97.setEnabled(False)
##########################################
    def return_purchase_removevendor(self):
        self.lineEdit_98.setText('')
        self.lineEdit_97.setEnabled(True)
        self.lineEdit_97.setText('')
########################################

    def return_purchase_search(self):

        barcode=self.lineEdit_72.text()
        name=self.lineEdit_73.text()
        self.cur.execute('''SELECT branch FROM default_branch''')
        branchs=self.cur.fetchall()
        branch=branchs[-1][0]
        fast_code=self.lineEdit_101.text()

        if name=='' and barcode == '' and fast_code=='' :
            QMessageBox.about(self,'caution','inter name or barcode or fast code')

        elif name=='' and fast_code=='' and barcode!='':

            self.cur.execute('''SELECT name, pur_price, req_quan,fast_code FROM items
            WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found1')
            else:
                name=data[0][0]
                self.lineEdit_73.setText(name)
                self.lineEdit_101.setText(str(data[0][3]))
                self.lineEdit_96.setText(str(data[0][1]))
                self.lineEdit_100.setText(str(data[0][2]))

        elif name!='' and barcode==''or  fast_code=='':
            self.cur.execute('''SELECT barcode, pur_price, req_quan,fast_code FROM items
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found2')
            else:
                self.lineEdit_72.setText(data[0][0])
                name=self.lineEdit_73.text()
                self.lineEdit_101.setText(str(data[0][3]))
                self.lineEdit_96.setText(str(data[0][1]))
                self.lineEdit_100.setText(str(data[0][2]))

        elif name=='' or barcode=='' and fast_code!='':
            self.cur.execute('''SELECT barcode,name, pur_price, req_quan FROM items
            WHERE fast_code=%s''',(fast_code))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','item not found3')
            else:
                name=data[0][1]
                self.lineEdit_73.setText(name)
                self.lineEdit_72.setText(data[0][0])
                self.lineEdit_96.setText(str(data[0][1]))
                self.lineEdit_100.setText(str(data[0][3]))

        elif name!='' and barcode != '' and fast_code!='' :
                self.cur.execute('''SELECT name, pur_price, req_quan,fast_code FROM items
                WHERE barcode=%s''',(barcode))
                data=self.cur.fetchall()
                if data==():
                    QMessageBox.about(self,'caution','item not found1')
                else:
                    name=data[0][0]
                    self.lineEdit_73.setText(name)
                    self.lineEdit_101.setText(str(data[0][3]))
                    self.lineEdit_96.setText(str(data[0][1]))
                    self.lineEdit_100.setText(str(data[0][2]))
        else:
            QMessageBox.about(self,'caution','choose different data for search')

        if data!=():
            self.cur.execute('''SELECT quantity FROM item_quant
                WHERE name=%s AND store=%s''',(name, branch))
            quants=self.cur.fetchall()
            if quants==():
                QMessageBox.about(self,'caution','not available balance1')
            else:
                self.lineEdit_75.setText(str(quants[0][0]))
                if quants[0][0]==0:
                    QMessageBox.about(self,'caution','not enough balance2')

                elif quants[0][0]<=data[0][2]:

                    self.lineEdit_84.setStyleSheet('background-color: rgb(255, 124, 166);')
                    self.lineEdit_41.setStyleSheet('background-color: rgb(255, 124, 166);')


                self.pushButton_62.setEnabled(True)

        else:
            pass
########################################

    def return_purchase_additem(self):#add item to the bill
        name=self.lineEdit_73.text()
        amount=self.lineEdit_74.text()
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        price=self.lineEdit_96.text()
        total_bill=0
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        self.cur.execute('''
        SELECT branch FROM default_branch
        ''')
        branchs = self.cur.fetchall()
        store=branchs[-1][0]
        balance=self.lineEdit_75.text()

        bill_id=self.lineEdit_103.text()#int(numbers[-1][0])+1

        if self.lineEdit_97.text()=='':
            cl_vend='cash'
        else:
            cl_vend=self.lineEdit_97.text()
        ########################################

        if amount=='':
            QMessageBox.about(self,'caution','inter desired amount')
            self.lineEdit_74.setFocus()
        elif not isfloat(amount) or not isfloat(price):
            QMessageBox.about(self,'caution','inter price & amount in numbers')
        else:
            total=(int(amount)*float(price))
            self.lineEdit_99.setText(str(total))

            self.cur.execute('''
                    INSERT INTO temp_bill(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,move)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',(name,amount,date,time,price,employee,store,total,bill_id,cl_vend,'rpur'))
            self.db.commit()

            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('rpur'))

            while self.tableWidget_9.rowCount()>0:
                self.tableWidget_9.removeRow(0)

            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                self.tableWidget_9.insertRow(row)
                total_bill+=float(data[4])
                self.lineEdit_77.setText(str(total_bill))
                for col, item in enumerate(data):
                    self.tableWidget_9.setItem(row,col,QTableWidgetItem(str(item)))

            self.pushButton_62.setEnabled(False)
            self.pushButton_73.setEnabled(True)

            self.lineEdit_72.setText('')
            self.lineEdit_101.setText('')
            self.lineEdit_73.setText('')
            self.lineEdit_74.setText('')
            self.lineEdit_96.setText('')
            self.lineEdit_99.setText('')
            self.lineEdit_75.setText('')
            self.lineEdit_100.setText('')
            self.lineEdit_72.setFocus()

#####################################

    def return_purchase_removeitem(self):
        
        
        item_id=self.lineEdit_102.text()
        total_bill=0
        self.cur.execute('''SELECT id, total FROM temp_bill WHERE id=%s AND move=%s''',(item_id,'rpur'))
        check=self.cur.fetchall()

        if item_id=='':
            QMessageBox.about(self,'caution','inter ID first')
            self.lineEdit_102.setFocus()
        elif check==():
            QMessageBox.about(self,'caution','inter correct ID')
            self.lineEdit_102.setFocus()
        else:
            total=check[0][1]
            self.cur.execute('''DELETE FROM temp_bill WHERE id=%s AND move=%s''',(item_id, 'rpur'))
            self.db.commit()
            while self.tableWidget_9.rowCount()>0:
                    self.tableWidget_9.removeRow(0)
            self.cur.execute('''SELECT id,name,amount,price,total
                            FROM temp_bill WHERE move=%s''',('rpur'))
            datas=self.cur.fetchall()
            for row , data in enumerate(datas):
                total_bill+=float(data[4])
                self.lineEdit_77.setText(str(total_bill))
                self.tableWidget_9.insertRow(row)
                for col, item in enumerate(data):
                    self.tableWidget_9.setItem(row,col,QTableWidgetItem(str(item)))
            self.lineEdit_102.setText('')
        self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('rpur'))
        check=self.cur.fetchall()
        if check==():
            self.pushButton_73.setEnabled(False)
            self.lineEdit_77.setText('0')
            
##########################################################

    def return_purchase_return(self):#save the bill
        if self.lineEdit_103.text()=='':
            self.show_returnpur()
        comment=self.lineEdit_109.text()
        bill_total=self.lineEdit_77.text()
        paid=self.lineEdit_76.text()
        cl_vend=self.lineEdit_97.text()
        ###########################move to main table
        if self.lineEdit_76.text()=='':
            QMessageBox.about(self,'caution', 'inter money paid')
            self.lineEdit_76.setFocus()
        elif not isfloat(self.lineEdit_76.text()):
            QMessageBox.about(self,'caution', 'inter only numbers')
            self.lineEdit_76.setFocus()
        elif cl_vend=='' and float(bill_total)!=float(paid):
            QMessageBox.about(self,'caution', 'you must pay all the money')
            self.lineEdit_76.setFocus()
        else:
            self.cur.execute('''SELECT * FROM temp_bill WHERE move=%s''',('rpur'))
            bill_items=self.cur.fetchall()
            for item in bill_items:
                name=item[1]
                amount=item[2]
                date=item[3]
                time=item[4]
                price=item[5]
                employee=item[6]
                store=item[7]
                total=item[8]
                bill_id=item[9]
                cl_vend=item[10]
                self.cur.execute('''INSERT INTO items_pur_ret(name,amount,date,
                time,price,employee,store,total,bill_id,vendor,comment)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (name,amount,date,time,price,employee,store,total,bill_id,cl_vend,comment))
                self.db.commit()
            ##################################fill quantity table
                self.cur.execute('''SELECT name, quantity FROM item_quant
                WHERE name=%s AND store=%s''',(name,store))
                check=self.cur.fetchall()
                if check==():
                    self.cur.execute('''
                    INSERT INTO item_quant(name,quantity,store)
                    VALUES(%s,%s,%s)
                    ''',(name,amount,store))
                    self.db.commit()
                elif check != ():
                    quantity=float(check[0][1])-float(amount)
                    self.cur.execute('''UPDATE item_quant SET quantity=%s
                     WHERE name=%s AND store=%s
                ''',(quantity,name,store))
                self.db.commit()

                #######################empty table widget

            ########################################fill bill table
            number=bill_items[0][9]
            date=bill_items[0][3]
            time=bill_items[0][4]
            employee=bill_items[0][6]
            store=bill_items[0][7]
            move='rpur'
            cl_vend=bill_items[0][10]
            self.cur.execute(''' INSERT INTO bill_no(number,date,time,
            employee,store,move,cl_vend,bill_total) VALUES(%s,%s,%s,%s,%s,%s,%s,%s)''',
            (number,date,time,employee,store,move,cl_vend,bill_total))
##########################################################fill safe drawer
            amount=self.lineEdit_76.text()
            cl_vend=self.lineEdit_97.text()
            if cl_vend=='':
                cl_vend='cash'
               
                if float(self.lineEdit_77.text())!= float(self.lineEdit_76.text()):
                    QMessageBox.about(self,'caution','this is cash bill')
                else:
                    
                    self.cur.execute('''INSERT INTO drawer_moves(branch,
                    reason,amount,date,time,comment,employee,move,source)
                    VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(store,'rpur',
                    amount,date,time,comment,employee,'in',cl_vend))
                    self.empty_returnpurchase()
                    self.show_returnpur()
                        

            else:
                amount=float(self.lineEdit_77.text())-float(self.lineEdit_76.text())
                
                if amount > 0:
                    self.cur.execute('''INSERT INTO vendor_balance(name,
                    amount,date,time,move,reason,employee,branch,bill_id) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ''',(cl_vend,amount,date,time,'in','rpur',employee,store,bill_id))
                    
                    
                amount=self.lineEdit_76.text()
                self.cur.execute('''INSERT INTO drawer_moves(branch,reason,amount,
                date,time,comment,employee,move,source)
                VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (store,'rpur',amount,date,time,comment,employee,'in',cl_vend))
                self.empty_returnpurchase()
                self.show_returnpur()
               
                

#########################################

#####################################

##################################### report tab

    def show_employee_absence(self):#employee absence report
        name=self.comboBox_30.currentText()
        date1=self.dateEdit_16.date().toPyDate()
        date2=self.dateEdit_15.date().toPyDate()
        emp_absence=[]
        self.cur.execute(''' SELECT name,date,time_in,time_out,branch,comment
            FROM employee_absence
            WHERE name= %s AND date BETWEEN %s AND %s''',(name,date1,date2))
        emps=self.cur.fetchall()
        
        if emps ==():
            QMessageBox.about(self,'caution','no data')
        else:
            while self.tableWidget_12.rowCount()>0:
                self.tableWidget_12.removeRow(0)
                
            for row,emp in enumerate (emps):
                self.tableWidget_12.insertRow(row)
                duration=emp[3]-emp[2]
                
                for col ,data in enumerate(emp):
                    self.tableWidget_12.setItem(row,col,QTableWidgetItem(str(data)))
                    self.tableWidget_12.setItem(row,6,QTableWidgetItem(str(duration)))
                    
            emp_absence.append(['absence',str(name),str(date1),'to',str(date2)])
            emp_absence.append(['name','date','time','move','branch'])
            for i in emps:
                emp_absence.append([i[0],i[1],i[2],i[3],i[4]])
            return emp_absence

########################################################
    def print_absence(self):
        try:
            printreport(self.show_employee_absence())
            open_pdf('report.pdf')
        except:
            QMessageBox.about(self,'caution','cant show report')
#########################################################
    def show_employees_data(self):#show all employees in a branch
        branch= self.comboBox_26.currentText()
        self.cur.execute('''SELECT name,password, branch,dedicate,adminity,join_date,comment
                            FROM employees WHERE branch =%s''',(branch))
        emps=self.cur.fetchall()
        if emps==():
            QMessageBox.about(self,'caution','no data')
        else:
            while self.tableWidget_11.rowCount()>0:
                self.tableWidget_11.removeRow(0)
                
        for row,emp in enumerate(emps):
            self.tableWidget_11.insertRow(row)
            for col,data in enumerate(emp):
                self.tableWidget_11.setItem(row,col,QTableWidgetItem(str(data)))
#############################################################
        
    def show_expenses_report(self):#show expenses report
        while self.tableWidget_6.rowCount()>0:
            self.tableWidget_6.removeRow(0)
        date1=self.dateEdit_19.date().toPyDate()
        date2=self.dateEdit_18.date().toPyDate()
        reason=self.comboBox_18.currentText()
        source=self.comboBox_6.currentText()
        total=0
        move=self.comboBox_7.currentText()
        expenses_list=[]
        expenses_list.append(['','','','money moves','','',''])
        expenses_list.append(['amount','operation','date','time','reason','employee','comment','to/from'])
        
        
        if move =='IN':
            if source=='ALL':
                if reason=='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date ASC,time ASC''', ('in',date1,date2))
                    drawermoves=self.cur.fetchall()
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date ASC,time ASC''', ('in',date1,date2))
                    safemoves=self.cur.fetchall()
                    
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves ==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    if safemoves ==():
                        pass 
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                        
                    self.lineEdit_110.setText(str(total))
                    
                elif reason != 'ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',reason,date1,date2))
                    drawermoves=self.cur.fetchall()
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',reason,date1,date2))
                    safemoves=self.cur.fetchall()
                    
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                    self.lineEdit_110.setText(str(total))
                            
            elif source == 'SAFE':
                if reason=='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',date1,date2))
                    safemoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                    
                elif reason !='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',reason,date1,date2))
                    safemoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                    
                    self.lineEdit_110.setText(str(total))
                    
            elif source == 'DRAWER':
                if reason== 'ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',date1,date2))
                    drawermoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                    
                elif reason !='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('in',reason,date1,date2))
                    drawermoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                

        elif move=='OUT':
           if source=='ALL':
                if reason=='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',date1,date2))
                    drawermoves=self.cur.fetchall()
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',date1,date2))
                    safemoves=self.cur.fetchall()
                    
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves ==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    if safemoves ==():
                        pass 
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                    
                elif reason != 'ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',reason,date1,date2))
                    drawermoves=self.cur.fetchall()
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',reason,date1,date2))
                    safemoves=self.cur.fetchall()
                    
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                            
           elif source == 'SAFE':
               if reason=='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',date1,date2))
                    safemoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                    self.lineEdit_110.setText(str(total))
                    
               elif reason !='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM safe_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',reason,date1,date2))
                    safemoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if safemoves == ():
                        pass
                    else:
                        for row, move in enumerate(safemoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'safe'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('safe'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                    
           elif source == 'DRAWER':
                if reason== 'ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',date1,date2))
                    drawermoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                            
                            
                    self.lineEdit_110.setText(str(total))
                    
                elif reason !='ALL':
                    self.cur.execute(''' SELECT amount,source,date,time,reason,employee,comment
                    FROM drawer_moves WHERE move=%s AND reason=%s AND date BETWEEN %s AND %s ORDER BY date, time''', ('out',reason,date1,date2))
                    drawermoves=self.cur.fetchall()
                    while self.tableWidget_6.rowCount()>0:
                        self.tableWidget_6.removeRow(0)
                    if drawermoves==():
                        pass
                    else:
                        for row, move in enumerate(drawermoves):
                            expenses_list.append([str(move[0]),str(move[1]),str(move[2]),
                                                str(move[3]),str(move[4]),str(move[5]),str(move[6]),'drawer'])
                            self.tableWidget_6.insertRow(row)
                            total+= float(move[0])
                            for col, data in enumerate(move):
                                self.tableWidget_6.setItem(row,col,QTableWidgetItem(str(data)))
                                self.tableWidget_6.setItem(row,7,QTableWidgetItem('drawer'))
                        
                    self.lineEdit_110.setText(str(total))
        return expenses_list        
                    
 ###################################################################### 
    def print_expenses(self):
        try:
            printreport(self.show_expenses_report())
            open_pdf('report.pdf')
        except:
            QMessageBox.about(self,'caution','cant show report')
 ################################################################          

    def show_clients_report(self):#show client balance report
        name=self.comboBox_8.currentText()
        date1=self.dateEdit_20.date().toPyDate()
        date2=self.dateEdit_21.date().toPyDate()
        option=self.comboBox_13.currentText()
        balance=0
        while self.tableWidget_7.rowCount()>0:
            self.tableWidget_7.removeRow(0)
        if option=='ALL':
            self.cur.execute('''SELECT name,amount,date,time,move,reason,employee,branch,bill_id
            FROM client_balance WHERE name=%s AND date BETWEEN %s AND %s''',(name,date1,date2))
            moves=self.cur.fetchall()
            if moves == ():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_7.insertRow(row)
                    balance+=float(move[1])
                    for col,data in enumerate(move):
                        self.tableWidget_7.setItem(row,col,QTableWidgetItem(str(data)))
                self.lineEdit_35.setText(str(balance))
        else:
            self.cur.execute('''SELECT name,amount,date,time,move,reason,employee,branch,bill_id
            FROM client_balance WHERE name=%s AND reason =%s AND date BETWEEN %s AND %s''',(name,option,date1,date2))
            moves=self.cur.fetchall()
            if moves == ():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_7.insertRow(row)
                    balance+=float(move[1])
                    for col,data in enumerate(move):
                        self.tableWidget_7.setItem(row,col,QTableWidgetItem(str(data)))
                self.lineEdit_35.setText(str(balance))
###################################################################
    def show_vendors_report(self):#show vendor balance report
        name=self.comboBox_9.currentText()
        date1=self.dateEdit_22.date().toPyDate()
        date2=self.dateEdit_23.date().toPyDate()
        option=self.comboBox_5.currentText()
        balance=0
        while self.tableWidget_8.rowCount()>0:
            self.tableWidget_8.removeRow(0)
        if option=='ALL':
            self.cur.execute('''SELECT name,amount,date,time,move,reason,employee,branch,bill_id
            FROM vendor_balance WHERE name=%s AND date BETWEEN %s AND %s''',(name,date1,date2))
            moves=self.cur.fetchall()
            if moves == ():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_8.insertRow(row)
                    balance+=float(move[1])
                    for col,data in enumerate(move):
                        self.tableWidget_8.setItem(row,col,QTableWidgetItem(str(data)))
                self.lineEdit_36.setText(str(balance))
        else:
            self.cur.execute('''SELECT name,amount,date,time,move,reason,employee,branch,bill_id
            FROM vendor_balance WHERE name=%s AND reason= %s AND date BETWEEN %s AND %s''',(name,option,date1,date2))
            moves=self.cur.fetchall()
            if moves == ():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_8.insertRow(row)
                    balance+=float(move[1])
                    for col,data in enumerate(move):
                        self.tableWidget_8.setItem(row,col,QTableWidgetItem(str(data)))
            self.lineEdit_36.setText(str(balance))
####################################################################


    def show_items_fastreport(self):#show items fast quantity report in a branch
        barcode=self.lineEdit_6.text()
        fastcode=self.lineEdit_113.text()
        name=self.lineEdit_13.text()
        branch=self.comboBox.currentText()
        balance=0
        row=0
        fastreport_list=[]
        fastreport_list.append(['','quantities',str(branch),''])
        fastreport_list.append(['name','purchase price','sell price','quantity'])
        
        while self.tableWidget.rowCount()>0:
            self.tableWidget.removeRow(0)
       
       
        if name=='' and barcode=='' and fastcode=='':
            self.cur.execute('''SELECT name, pur_price, sell_price from items ''')
            items=self.cur.fetchall()
           
            if items==():
                QMessageBox.about(self,'caution','no items!')
            
            else:
                for item in items:
                    self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(item[0],branch))
                    quants=self.cur.fetchall()
                    if quants==():
                        pass
                    elif quants[0][0]==0:
                        pass
                    else:
                        fastreport_list.append([str(item[0]),str(item[1]),str(item[2]),str(quants[0][0])])
                        self.tableWidget.insertRow(row)
                        for col, data in enumerate(item):
                            self.tableWidget.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget.setItem(row,3,QTableWidgetItem(str(quants[0][0])))
                        
                        row+=1
                        
        
        elif name=='' and fastcode=='' and barcode!='':
            self.cur.execute('''SELECT name, pur_price, sell_price from items WHERE barcode=%s''',(barcode))
            items=self.cur.fetchall()
            
            if items==():
                QMessageBox.about(self,'caution','item not found')
            else:
                for row,item in enumerate(items):
                    self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(item[0],branch))
                    quants=self.cur.fetchall()
                    if quants==():
                        pass
                    elif quants[0][0]==0:
                        pass
                    else:
                        fastreport_list.append([str(item[0]),str(item[1]),str(item[2]),str(quants[0][0])])
                        self.tableWidget.insertRow(row)
                        for col, data in enumerate(item):
                            self.tableWidget.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget.setItem(row,3,QTableWidgetItem(str(quants[0][0])))
        
        elif name!='' and barcode==''or  fastcode=='':
            self.cur.execute('''SELECT name, pur_price, sell_price from items WHERE name=%s''',(name))
            items=self.cur.fetchall()
            
            if items==():
                QMessageBox.about(self,'caution','item not found')
            else:
                for row,item in enumerate(items):
                    self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(item[0],branch))
                    quants=self.cur.fetchall()
                    if quants==():
                        pass
                    elif quants[0][0]==0:
                        pass
                    else:
                        fastreport_list.append([str(item[0]),str(item[1]),str(item[2]),str(quants[0][0])])
                        self.tableWidget.insertRow(row)
                        for col, data in enumerate(item):
                            self.tableWidget.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget.setItem(row,3,QTableWidgetItem(str(quants[0][0])))
            
        
        elif name=='' or barcode=='' and fastcode!='':
            self.cur.execute('''SELECT name, pur_price, sell_price from items WHERE fast_code=%s''',(fastcode))
            items=self.cur.fetchall()
            
            if items==():
                QMessageBox.about(self,'caution','item not found')
            else:
                for row,item in enumerate(items):
                    self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(item[0],branch))
                    quants=self.cur.fetchall()
                    if quants==():
                        pass
                    elif quants[0][0]==0:
                        pass
                    else:
                        fastreport_list.append([str(item[0]),str(item[1]),str(item[2]),str(quants[0][0])])
                        self.tableWidget.insertRow(row)
                        for col, data in enumerate(item):
                            self.tableWidget.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget.setItem(row,3,QTableWidgetItem(str(quants[0][0])))
            
        
        
        elif name!='' and barcode != '' and fastcode!='' :
            self.cur.execute('''SELECT name, pur_price, sell_price from items WHERE barcode=%s''',(barcode))
            items=self.cur.fetchall()
            if items==():
                QMessageBox.about(self,'caution','item not found')
            else:
                for row,item in enumerate(items):
                    self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(item[0],branch))
                    quants=self.cur.fetchall()
                    if quants==():
                        pass
                    elif quants[0][0]==0:
                        pass
                    else:
                        fastreport_list.append([str(item[0]),str(item[1]),str(item[2]),str(quants[0][0])])
                        self.tableWidget.insertRow(row)
                        for col, data in enumerate(item):
                            self.tableWidget.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget.setItem(row,3,QTableWidgetItem(str(quants[0][0])))
        return fastreport_list
##############################################################################
    def print_items_fast_report(self):
        try:
            printreport(self.show_items_fastreport())
            open_pdf('report.pdf')
        except:
            QMessageBox.about(self,'caution','cant show report')
        

##################################################################################

    def show_items_movementreport(self):#show items movements report
        barcode=self.lineEdit_8.text()
        name=self.lineEdit_16.text()
        fastcode=self.lineEdit_114.text()
        store=self.comboBox_14.currentText()
        date1=self.dateEdit_10.date().toPyDate()
        date2=self.dateEdit_17.date().toPyDate()
        operation=self.comboBox_22.currentText()
        print_data=[]
        
        
        
        while self.tableWidget_2.rowCount()>0:
            self.tableWidget_2.removeRow(0)
        while self.tableWidget_10.rowCount()>0:
            self.tableWidget_10.removeRow(0)
        
        if name=='' and barcode=='' and fastcode=='':
            QMessageBox.about(self,'caution','inter data to search for!')
        elif name=='' and fastcode=='' and barcode!='':
            self.cur.execute('''SELECT name,fast_code FROM items WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found!')
            else:
                self.lineEdit_16.setText(str(data[0][0]))
                self.lineEdit_114.setText(str(data[0][1]))
        elif name!='' and barcode==''or  fastcode=='':
            self.cur.execute('''SELECT barcode,fast_code FROM items WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found!')
            else:
                self.lineEdit_8.setText(str(data[0][0]))
                self.lineEdit_114.setText(str(data[0][1]))
        elif name=='' or barcode=='' and fastcode!='':
            self.cur.execute('''SELECT barcode,name FROM items WHERE fast_code=%s''',(fastcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found!')
            else:
                self.lineEdit_8.setText(str(data[0][0]))
                self.lineEdit_16.setText(str(data[0][1]))
        elif name!='' and barcode != '' and fastcode!='':
            self.cur.execute('''SELECT name,fast_code FROM items WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found!')
            else:
                self.lineEdit_16.setText(str(data[0][0]))
                self.lineEdit_114.setText(str(data[0][1]))
        else:
            QMessageBox.about(self,'caution','inter data to search for!')
            
        
        name=self.lineEdit_16.text() 
        self.cur.execute('''SELECT quantity from item_quant WHERE name=%s AND store=%s''',(name,store))
        quants=self.cur.fetchone()
        if quants==None:
            pass
        else:
            self.lineEdit_10.setText(str(quants[0]))
            print_data.append(['','','items','movement','balance',str(quants[0]),'',''])
        
        if operation=='ALL':
            self.tabWidget_4.setCurrentIndex(0)
            self.cur.execute('''SELECT name,amount,date,time,vendor,employee,price FROM items_pur
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            purs=self.cur.fetchall()
            self.cur.execute('''SELECT name,amount,date,time,client,employee,price FROM items_sell
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            sells=self.cur.fetchall()
            self.cur.execute('''SELECT name,amount,date,time,vendor,employee,price FROM items_pur_ret
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            rpurs=self.cur.fetchall()
            self.cur.execute('''SELECT name,amount,date,time,client,employee,price FROM items_sell_ret
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            rsells=self.cur.fetchall()
            
            print_data.append(['name','quantity','date','time','ven/cl','employee','price','operation'])
            
            if purs==():
                pass
            else:
                for row,pur in enumerate(purs):
                    pur_data=[]
        
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(pur):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('PURCHASE'))
                        pur_data.append(str(data))
                    pur_data.append('purchase')
                    print_data.append(pur_data)
                    
            if sells==():
                pass
            else:
                for row,sell in enumerate(sells):
                    sell_data=[]
       
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(sell):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('SELL'))
                        sell_data.append(str(data))
                    sell_data.append('sell')
                    print_data.append(sell_data)
            if rpurs==():
                pass
            else:
                for row,rpur in enumerate(rpurs):
                    rpur_data=[]
        
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(rpur):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('R-PURCHASE'))
                        rpur_data.append(str(data))
                    rpur_data.append('r-purchase')
                    print_data.append(rpur_data)
            if rsells==():
                pass
            else:
                for row,rsell in enumerate(rsells):
                    rsell_data=[]
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(rsell):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('R-SELL'))
                        rsell_data.append(str(data))
                    rsell_data.append('r-sell')
                    print_data.append(rsell_data)
            
        elif operation=='PURCHASE':
            self.tabWidget_4.setCurrentIndex(0)
            self.cur.execute('''SELECT name,amount,date,time,vendor,employee,price FROM items_pur
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            purs=self.cur.fetchall()
            if purs==():
                pass
            else:
                for row,pur in enumerate(purs):
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(pur):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('PURCHASE'))
        elif operation=='SELL':
            self.tabWidget_4.setCurrentIndex(0)
            self.cur.execute('''SELECT name,amount,date,time,client,employee,price FROM items_sell
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            sells=self.cur.fetchall()
            if sells==():
                pass
            else:
                for row,sell in enumerate(sells):
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(sell):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('SELL'))
        elif operation=='R-PURCHASE':
            self.tabWidget_4.setCurrentIndex(0)
            self.cur.execute('''SELECT name,amount,date,time,vendor,employee,price FROM items_pur_ret
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            rpurs=self.cur.fetchall()
            if rpurs==():
                pass
            else:
                for row,rpur in enumerate(rpurs):
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(rpur):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('R-PURCHASE'))
        elif operation=='R-SELL':
            self.tabWidget_4.setCurrentIndex(0)
            self.cur.execute('''SELECT name,amount,date,time,client,employee,price FROM items_sell_ret
            WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name,store,date1,date2))
            rsells=self.cur.fetchall()
            if rsells==():
                pass
            else:
                for row,rsell in enumerate(rsells):
                    self.tableWidget_2.insertRow(row)
                    for col,data in enumerate(rsell):
                        self.tableWidget_2.setItem(row,col,QTableWidgetItem(str(data)))
                        self.tableWidget_2.setItem(row,7,QTableWidgetItem('R-SELL'))
                        
        elif operation=='MOVE':
            self.tabWidget_4.setCurrentIndex(1)
            self.cur.execute('''SELECT name,amount,date,time,employee,store2 FROM items_moves
            WHERE name=%s AND store1=%s AND operation=%s AND date BETWEEN %s AND %s''',(name,store,'move',date1,date2))
            moves=self.cur.fetchall()
            if moves==():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_10.insertRow(row)
                    for col,data in enumerate(move):
                        self.tableWidget_10.setItem(row,col,QTableWidgetItem(str(data)))
        else:
            self.tabWidget_4.setCurrentIndex(1)
            self.cur.execute('''SELECT name,amount,date,time,employee,reason,move FROM items_moves
            WHERE name=%s AND store1=%s AND operation=%s AND date BETWEEN %s AND %s''',(name,store,'edit',date1,date2))
            moves=self.cur.fetchall()
            if moves==():
                pass
            else:
                for row,move in enumerate(moves):
                    self.tableWidget_10.insertRow(row)
                    for col,data in enumerate(move):
                        self.tableWidget_10.setItem(row,col,QTableWidgetItem(str(data)))
        return print_data
####################################################3
    def print_item_movement(self):
        try:
            printreport(self.show_items_movementreport())
            open_pdf('report.pdf')
        except:
            QMessageBox.about(self,'caution','cant show report')
##################################################################

    def show_zeros_report(self):
        
        store=self.comboBox_42.currentText()
        while self.tableWidget_21.rowCount()>0:
            self.tableWidget_21.removeRow(0)
            
        if self.radioButton.isChecked():
            self.cur.execute('''SELECT name FROM item_quant WHERE store=%s AND quantity=%s''',(store,0))
            items=self.cur.fetchall()
            if items==():
                pass
            else:
                for row, item in enumerate( items):
                    self.tableWidget_21.insertRow(row)
                    if item==None:
                        pass
                    else:
                        self.cur.execute('''SELECT name,pur_price,sell_price,comment,req_quan FROM items WHERE name=%s''',(item[0]))
                        datas=self.cur.fetchone()
                        for col,data in enumerate(datas):
                            self.tableWidget_21.setItem(row,col,QTableWidgetItem(str(data)))
                            self.tableWidget_21.setItem(row,5,QTableWidgetItem(str(0)))
                            
        elif self.radioButton_2.isChecked():
            row=0
            
            self.cur.execute('''SELECT name, quantity FROM item_quant WHERE store=%s ''',(store))
            quants=self.cur.fetchall()
           
            for quant in quants:
                self.cur.execute('''SELECT name,pur_price,sell_price,req_quan,comment FROM items WHERE name=%s''',(quant[0]))
                datas=self.cur.fetchall()
                for data in  datas:
                    if int(data[3])>= int(quant[1]):
                        self.tableWidget_21.insertRow(row)
                        self.cur.execute('''SELECT name,pur_price,sell_price,comment,req_quan FROM items WHERE name=%s''',(quant[0]))
                        items=self.cur.fetchone()
                        for col,item in enumerate(items):
                            self.tableWidget_21.setItem(row,col,QTableWidgetItem(str(item)))
                            self.tableWidget_21.setItem(row,5,QTableWidgetItem(str(quant[1])))
                        row+=1
                    else:
                        pass
                            
                        
######################################################

    def show_bills_report(self):
        bill_no=self.lineEdit_124.text()
        operation=self.comboBox_44.currentText()
        branch=self.comboBox_45.currentText()
        date1=self.dateEdit_12.date().toPyDate()
        date2=self.dateEdit_33.date().toPyDate()
        bills_toprint=[]
        movedict={'pur':'purchase', 'sell':'sell','rpur':'return purchase','rsell':'return sell'}
        bills_toprint.append([movedict.get(operation),'report','from',str(date1),'to',str(date2)])
        bills_toprint.append(['bill no.','date','time','employee','cl-vend','total'])
        while self.tableWidget_22.rowCount()>0:
            self.tableWidget_22.removeRow(0)
        while self.tableWidget_23.rowCount()>0:
            self.tableWidget_23.removeRow(0)
            
        if bill_no!='':
            self.tabWidget_7.setCurrentIndex(0)
            self.cur.execute('''SELECT number,date,time,employee,cl_vend,bill_total
            FROM bill_no WHERE number=%s AND move=%s AND store=%s AND date BETWEEN %s AND %s''',(bill_no,operation,branch,date1,date2))
            bills=self.cur.fetchall()
            if bills==():
                QMessageBox.about(self,'caution','bill not found')
            else:
                for row,bill in enumerate(bills):
                    self.tableWidget_22.insertRow(row)
                    for col,data in enumerate(bill):
                        self.tableWidget_22.setItem(row,col,QTableWidgetItem(str(data)))
        else:
            self.tabWidget_7.setCurrentIndex(0)
            self.cur.execute('''SELECT number,date,time,employee,cl_vend,bill_total
            FROM bill_no WHERE move=%s AND store=%s AND date BETWEEN %s AND %s''',(operation,branch,date1,date2))
            bills=self.cur.fetchall()
            if bills==():
                QMessageBox.about(self,'caution','bill not found')
            else:
                for row,bill in enumerate(bills):
                    bill_item=[]
                    self.tableWidget_22.insertRow(row)
                    for col,data in enumerate(bill):
                        self.tableWidget_22.setItem(row,col,QTableWidgetItem(str(data)))
                        bill_item.append(str(data))
                    bills_toprint.append(bill_item)
                return bills_toprint
#####################################################
    def print_bills(self):
        try:
            printreport(self.show_bills_report())
            open_pdf('report.pdf')
        except:
            pass
                    
#########################################################
    def show_bill_detailreport(self):
        bill_no=self.lineEdit_125.text()
        operation=self.comboBox_44.currentText()
        branch=self.comboBox_45.currentText()
        movedict={'pur':'purchase', 'sell':'sell','rpur':'return purchase','rsell':'return sell'}
        values_toprint=[]
        
        
        while self.tableWidget_23.rowCount()>0:
            self.tableWidget_23.removeRow(0)

        if bill_no=='':
            QMessageBox.about(self,'caution','inter bill no.')
        else:
            self.tabWidget_7.setCurrentIndex(1)
            if operation=='sell':
                self.cur.execute('''SELECT name,amount,price,total,comment FROM items_sell
                WHERE bill_id=%s AND store=%s''',(bill_no,branch))
                details=self.cur.fetchall()
                self.cur.execute('''SELECT date,time,cl_vend,bill_total FROM bill_no WHERE number=%s AND move=%s''',(bill_no,'sell'))
                total=self.cur.fetchall()
                
                
            elif operation=='rsell':
                self.cur.execute('''SELECT name,amount,price,total,comment FROM items_sell_ret
                WHERE bill_id=%s AND store=%s''',(bill_no,branch))
                details=self.cur.fetchall()
                self.cur.execute('''SELECT date,time,cl_vend,bill_total FROM bill_no WHERE number=%s AND move=%s''',(bill_no,'rsell'))
                total=self.cur.fetchall()
                
            elif operation=='pur':
                self.cur.execute('''SELECT name,amount,price,total,comment FROM items_pur
                WHERE bill_id=%s AND store=%s''',(bill_no,branch))
                details=self.cur.fetchall()
                self.cur.execute('''SELECT date,time,cl_vend,bill_total FROM bill_no WHERE number=%s AND move=%s''',(bill_no,'pur'))
                total=self.cur.fetchall()
                
            elif operation=='rpur':
                self.cur.execute('''SELECT name,amount,price,total,comment FROM items_pur_ret
                WHERE bill_id=%s AND store=%s''',(bill_no,branch))
                details=self.cur.fetchall()
                self.cur.execute('''SELECT date,time,cl_vend,bill_total FROM bill_no WHERE number=%s AND move=%s''',(bill_no,'rpur'))
                total=self.cur.fetchall()
            
            if details==():
                QMessageBox.about(self,'caution','not found')
            else:
                self.lineEdit_128.setText(str(total[0][2]))
                self.lineEdit_133.setText(str(total[0][0]))
                self.lineEdit_132.setText(str(total[0][1]))
                self.lineEdit_129.setText(str(total[0][3]))
                values_toprint.append([str(movedict.get(operation))+'-'+str(bill_no),self.lineEdit_128.text(),
                self.lineEdit_133.text(),self.lineEdit_132.text(),self.lineEdit_129.text()])
                values_toprint.append(['name','quantity','price','total','comment'])
                
                for row,detail in enumerate(details):
                    value=[]
                    self.tableWidget_23.insertRow(row)
                    for col,data in enumerate(detail):
                        self.tableWidget_23.setItem(row,col,QTableWidgetItem(str(data)))
                        value.append(data)
                    values_toprint.append(value)
            
            return values_toprint
 ###############################################################
    def print_bill_details(self):
        try:
            printreport(self.show_bill_detailreport())
            open_pdf('report.pdf')
        except:
            pass
##########################################################
 
    def show_assold_report(self):
        branch=self.comboBox_46.currentText()
        date1=self.dateEdit_13.date().toPyDate()
        date2=self.dateEdit_34.date().toPyDate()
        old_period=(date2-date1).days
        total_bill=0
        new_period=int(self.lineEdit_126.text())
        itemslist=[]
        deposlist=[]
        old_quants=[]
        row=0
        totals=0
        purchase_list=[]
        
        while self.tableWidget_24.rowCount()>0:
            self.tableWidget_24.removeRow(0)
        
        if self.lineEdit_126.text()=='':
            QMessageBox.about(self,'caution','inter number of days')
            self.lineEdit_126.setFocus()
        elif not isint(new_period) or new_period=='':
            QMessageBox.about(self,'caution','inter number of days')
        elif old_period<=0:
            QMessageBox.about(self,'caution','inter correct dates')
        else:
            self.cur.execute('''SELECT name FROM depository WHERE belong=%s''',(branch))
            depos=self.cur.fetchall()
            deposlist.append(branch)
            for depo in depos:
                deposlist.append(depo[0])
            
            self.cur.execute('''SELECT name FROM items''')
            names=self.cur.fetchall()
            for name in names:
                balance=0
                total=0
                self.cur.execute('''SELECT SUM(amount) FROM items_sell
                WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name[0], branch,date1,date2))
                amounts=self.cur.fetchall()
                print (amounts)
                if amounts[0][0]==None:
                    continue
                else:
                    total+=float(amounts[0][0])
              
                    self.cur.execute('''SELECT pur_price,sell_price,comment FROM items
                                        WHERE name=%s''',(name[0]))
                    details=self.cur.fetchall()
               
                    self.cur.execute('''SELECT SUM(quantity) FROM item_quant WHERE name=%s AND store in %s''',(name[0],deposlist))
                    quants=self.cur.fetchall()
                    balance+=float(quants[0][0])
                    
                    
                    old_quants.append(balance)
                    
                    itemslist.append([name[0],ceil(total/old_period)*new_period,details[0][0],details[0][1]])
            printlist=[]
            printlist.append(['quantity','enough for',str(new_period)+' days','based on','sales from',str(date1),'to '+str(date2)])
            printlist.append(['name','quantity','purchase price','sell price','exist quantity','required','total'])
            for (items,old) in zip(itemslist,old_quants):
                
                if items[1]> old:
                    req=items[1]-old
                    self.tableWidget_24.insertRow(row)
                    total_bill=req*items[2]
                    totals+=total_bill
                    purchase_list.append([items[0],req,items[2],total_bill])
                    printlist.append([str(items[0]),str(items[1]),str(items[2]),str(items[3]),str(old),str(req),str(total_bill)])
                    for col,item in enumerate(items):
                        self.tableWidget_24.setItem(row,col,QTableWidgetItem(str(item)))
                        self.tableWidget_24.setItem(row,4,QTableWidgetItem(str(old)))
                        self.tableWidget_24.setItem(row,5,QTableWidgetItem(str(req)))
                        self.tableWidget_24.setItem(row,6,QTableWidgetItem(str(total_bill)))
           
                    row+=1
                
                self.lineEdit_127.setText(str(totals))            
                
            return [purchase_list,printlist]
               
            
############################################################# 
    def print_assold(self):
        try:
            printreport(self.show_assold_report()[1])
            open_pdf('report.pdf')
        except:
            pass
        
##########################################################
        
    def send_topurchase(self):
        order=(self.show_assold_report()[0])
        new_order=[]
        date=datetime.date.today()
        time=datetime.datetime.now().strftime('%H:%M')
        self.cur.execute('''
            SELECT employee FROM default_employee
            ''')
        emps = self.cur.fetchall()
        employee=emps[-1][0]
        store=self.comboBox_46.currentText()
        self.cur.execute('''SELECT number FROM bill_no''')
        nums=self.cur.fetchall()
        bill_id=str(int(nums[-1][0])+1)
        if self.lineEdit_130.text()=='':
            cl_vend='cash'
        else:
            cl_vend=self.lineEdit_130.text()
            
        if order==[]:
            pass
        else:
          
            for line in order:
                new_order.append([line[0],line[1],date,time,line[2],employee,store,line[3],bill_id,cl_vend,'pur'])
            
            for data in new_order:
                self.cur.execute('''INSERT INTO temp_bill(name,amount,date,time,price,employee,
                store,total,bill_id,cl_vend,move) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''',
                (data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10]))
                
            self.lineEdit_69.setText(cl_vend)
            self.lineEdit_70.setText(self.lineEdit_131.text())
            self.lineEdit_71.setText(bill_id)
        
            self.show_purchase()
                    
 ##########################################
    def send_topurchase_showvendor(self):#show vendor money balance
        name=self.lineEdit_130.text()

        if name=='':
            QMessageBox.about(self, 'caution', 'inter vendor name')
        else:
            self.cur.execute(''' SELECT name FROM vendors
            WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self, 'caution', 'cant find vendor')
            else:
                qin=0
                qout=0
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'in'))
                allin=self.cur.fetchall()
                for i in allin:
                    qin+=float(i[0])
                self.cur.execute('''select amount FROM vendor_balance
                WHERE name=%s AND move=%s''',(name,'out'))
                allout=self.cur.fetchall()
                for i in allout:
                    qout+=float(i[0])
                balance=qout-qin
                self.lineEdit_131.setText(str(balance))
                self.lineEdit_130.setEnabled(False)       
 ###################################################
    def send_topurchase_removevendor(self):
        self.lineEdit_131.setText('')
        self.lineEdit_130.setEnabled(True)
        self.lineEdit_130.setText('')       
            
#############################################3
    def show_profit_tab(self):
        branch=self.comboBox_47.currentText()
        date1=self.dateEdit_14.date().toPyDate()
        date2=self.dateEdit_35.date().toPyDate()
        profit=0
        allsales=0
        expenses=0
        self.cur.execute('''SELECT name FROM items ''')
        names=self.cur.fetchall()
        table=[]
        printdata=[]
        while self.tableWidget_13.rowCount()>0:
            self.tableWidget_13.removeRow(0)
        if (date2-date1).days <1:
            QMessageBox.about(self,'caution','inter prober period')
        else:
            for name in names:
               
                self.cur.execute('''SELECT SUM(price*amount)/SUM(amount) FROM items_pur
                WHERE name=%s AND store=%s ''',(name[0],branch))
                pur_medians=self.cur.fetchall()
            
                self.cur.execute('''SELECT SUM(price*amount)/SUM(amount),SUM(amount) FROM items_sell
                WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name[0],branch,date1,date2))
                sell_medians=self.cur.fetchall()
                
                for (pur_median,sell_median) in zip(pur_medians,sell_medians):
                    if pur_median[0]==None or sell_median[0]==None:
                        continue
                    else:
                        profit+=(float(sell_median[0])-float(pur_median[0]))*float(sell_median[1])
                    
                self.cur.execute('''SELECT SUM(price*amount) FROM items_sell 
                WHERE name=%s AND store=%s AND date BETWEEN %s AND %s''',(name[0],branch,date1,date2))
                sales=self.cur.fetchall()
                for sale in sales:
                    if sale[0]==None:
                        pass
                    else:
                        allsales+=sale[0]
    
            self.cur.execute('''SELECT SUM(amount) FROM drawer_moves 
            WHERE branch = %s AND reason != %s AND reason != %s AND reason != %s AND move = %s AND date BETWEEN %s AND %s''',
            ( branch,'pur','rsell','to safe','out',date1,date2))
            drawer_expenses=self.cur.fetchall()
            if drawer_expenses[0][0]==None:
                pass
            else:
                expenses+=float(drawer_expenses[0][0])
            self.cur.execute('''SELECT SUM(amount) FROM safe_moves 
            WHERE branch = %s AND reason != %s AND reason != %s AND reason != %s AND move=%s AND date BETWEEN %s AND %s''',
            ( branch,'pur','rsell','to drawer','out',date1,date2))
            safe_expenses=self.cur.fetchall()
            if safe_expenses[0][0]==None:
                pass
            else:
                expenses+=float(safe_expenses[0][0])
                
            netprofit=profit-expenses
            table.append(str(date1))
            table.append(str(date2))
            table.append(str(allsales))
            table.append(str(profit))
            table.append(str(expenses))
            table.append(str(netprofit))
           
            self.tableWidget_13.insertRow(0)
            for col,item in enumerate(table):
                self.tableWidget_13.setItem(0,col,QTableWidgetItem(str(item)))
            printdata.append(['','','','profit report','',''])
            printdata.append(['startdate','enddate','sales','gross','expenses','net'])
            printdata.append(table)
            return printdata
############################################################
    def print_profit(self):
        try:
            printreport(self.show_profit_tab())
            open_pdf('report.pdf')
        except:
            QMessageBox.about(self,'caution','cant show report')
############################################################        
    def show_item_forbarcode(self):
        barcode=self.lineEdit_116.text()
        fastcode=self.lineEdit_115.text()
        name=self.lineEdit_20.text()
        branch=self.comboBox_48.currentText()
        
        if barcode=='' and name=='' and fastcode=='':
            QMessageBox.about(self,'caution','inter data to search')
        elif barcode!='' and name=='' and fastcode=='':
            self.cur.execute('''SELECT name, fast_code FROM items WHERE barcode=%s''',(barcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found')
            else:
                self.lineEdit_20.setText(data[0][0])
                self.lineEdit_115.setText(data[0][1])
        elif fastcode!='' and barcode=='' and name=='':
            self.cur.execute('''SELECT name, barcode FROM items WHERE fast_code=%s''',(fastcode))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found')
            else:
                self.lineEdit_20.setText(data[0][0])
                self.lineEdit_116.setText(data[0][1])
        elif name!='' and barcode=='' and fastcode=='':
            self.cur.execute('''SELECT barcode, fast_code FROM items WHERE name=%s''',(name))
            data=self.cur.fetchall()
            if data==():
                QMessageBox.about(self,'caution','not found')
            else:
                self.lineEdit_116.setText(data[0][0])
                self.lineEdit_115.setText(data[0][1])
        else:
            QMessageBox.about(self,'caution','inter 1 data')
        
        name=self.lineEdit_20.text()
        self.cur.execute('''SELECT quantity FROM item_quant WHERE name=%s AND store=%s''',(name, branch))
        quants=self.cur.fetchall()
        if name=='':
            pass
        elif quants==():
            QMessageBox.about(self,'caution','no quantity')
        else:
            self.lineEdit_117.setText(str(quants[0][0]))
            self.lineEdit_20.setEnabled(False)
            self.lineEdit_115.setEnabled(False)
            self.lineEdit_116.setEnabled(False)
            
        
#############################################################
    def add_item_forbarcode(self):
        name=self.lineEdit_20.text()
        barcode=self.lineEdit_116.text()
        amount=self.lineEdit_118.text()
        while self.tableWidget_25.rowCount()>0:
            self.tableWidget_25.removeRow(0)
        if amount=='':
            QMessageBox.about(self,'caution','inter desired amount')
            self.lineEdit_118.setFocus()
        else:
            self.cur.execute('''INSERT INTO barcode_table(barcode,name,amount)
            VALUES(%s,%s,%s)''',(barcode,name,amount))
            self.db.commit()
            self.cur.execute('''SELECT barcode,name,amount FROM barcode_table''')
            items=self.cur.fetchall()
            for row,item in enumerate(items):
                self.tableWidget_25.insertRow(row)
                for col,data in enumerate(item):
                    self.tableWidget_25.setItem(row,col,QTableWidgetItem(str(data)))
            self.lineEdit_20.setEnabled(True)
            self.lineEdit_115.setEnabled(True)
            self.lineEdit_116.setEnabled(True)        
            self.lineEdit_116.setText('')
            self.lineEdit_115.setText('')
            self.lineEdit_20.setText('')
            self.lineEdit_118.setText('')

###########################################################
    def print_barcode(self):
        
        self.cur.execute('''SELECT barcode,amount FROM barcode_table''')
        barcodes=self.cur.fetchall()
        if barcodes==():
            pass
        else:
            for f,barcode in enumerate(barcodes):
                slist=[]
                for num ,i in enumerate(range(barcode[1])):
                    bar=EAN13(barcode[0]+'000000000')
                    bar.save(str(f)+str(num))
                    
            while self.tableWidget_25.rowCount()>0:
                self.tableWidget_25.removeRow(0)
        
       
###########################################
def printreport(x):
    pdf=SimpleDocTemplate('report.pdf',pagesize=A4,topMargin=20,bottomMargin=20,leftMargin=20,rightMargin=20)
    style=TableStyle([
        ('BACKGROUND',(0,2),(-1,-1),colors.beige),
        ('BACKGROUND',(0,1),(-1,1),colors.burlywood),
        ('ALIGN',(0,0),(-1,-1),('CENTER')),
        ('ALIGN',(0,0),(0,0),('CENTER')),
        ('FONTSIZE',(0,0),(-1,-1),12),
        ('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('BOTTOMPADDING',(0,0),(-1,0),12),
        ('BOX',(0,1),(-1,-1),1,colors.black),
        ('GRID',(0,1),(-1,-1),1,colors.black)
        
        ])
    elems=[]
    report=Table(x)
    report.setStyle(style)
    elems.append(report)
    pdf.build(elems)
#################################################
def open_pdf(x):
    if platform.system()=='Linux':
        subprocess.call(['xdg-open',x])
    else:
        os.startfile(x)

#####################################
def autocomplete(items,place):
    completer=QCompleter(items)
    place.setCompleter(completer)

#####################################

def main():
    app=QApplication(sys.argv)
    window=Main()
    window.show()
    app.exec_()
if __name__=='__main__':
    main()
