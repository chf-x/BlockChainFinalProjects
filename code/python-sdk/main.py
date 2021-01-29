from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import QDateTime
from PyQt5.QtWidgets import QMessageBox,QMainWindow, QTableWidgetItem
from gui.bank import Ui_Bank
from gui.companies import Ui_Companies
from gui.login import Ui_Login
from gui.signup import Ui_Signup
import os,sys,json,glob
from client.contractnote import ContractNote
from client.bcosclient import BcosClient
from eth_utils import to_checksum_address
from eth_utils.hexadecimal import encode_hex
from eth_account.account import Account
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client.bcoserror import BcosException, BcosError
from client_config import client_config
    
def hex_to_signed(source):
    """
    将返回的十六进制整数转化为有符号整数，便于程序继续判断
    """
    if not isinstance(source, str):
        raise ValueError("string type required")
    if 0 == len(source):
        raise ValueError("string is empty")
    source = source[2:]
    sign_bit_mask = 1 << (len(source)*4-1)
    other_bits_mask = sign_bit_mask - 1
    value = int(source, 16)
    return -(value & sign_bit_mask) | (value & other_bits_mask)

class Bank(QMainWindow, Ui_Bank):
    def __init__(self, parent=None):
        super(Bank, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Bank")
        self.btn_authorize.clicked.connect(self.authorize)
        self.btn_quit.clicked.connect(self.quit)
        self.btn_reject.clicked.connect(self.reject)
        self.table.setColumnCount(5) 
        # 设置交易信息列表表头
        self.headers = ['From','To','Amount','Status','Due date']
        self.table.setHorizontalHeaderLabels(self.headers)
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    def set_table_content(self):
        global client, contract_abi, to_address
        # 调用合约函数selectFromReceipt
        result = client.call(to_address, contract_abi, "selectFromReceipt", ["", 2])
        # 在中断打印信息，便于调试
        print("receipt:",result)
        row_lenth = len(result[0])
        # 显示信息
        for i in range(row_lenth):
            row = self.table.rowCount()
            self.table.setRowCount(row + 1)
            self.table.setItem(row,0,QTableWidgetItem(result[0][i]))
            self.table.setItem(row,1,QTableWidgetItem(result[1][i]))
            self.table.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table.setItem(row,4,QTableWidgetItem(result[4][i]))
    
    # 定义银行的认证功能
    def authorize(self):
        global client, contract_abi, to_address
        if self.table.selectionModel().hasSelection():
            row = self.table.currentRow()
            args = [self.table.item(row, 0).text(), self.table.item(row, 1).text(), \
                int(self.table.item(row, 2).text()), "authorized",self.table.item(row, 4).text()]
            print(args)
            # 调用合约函数 update ，将信息更新为 "authorized"
            result = client.sendRawTransactionGetReceipt(to_address, contract_abi, "update", args)
            print("receipt:",result)
            QMessageBox.information(self,'Prompt','Success', QMessageBox.Ok)
            self.table.setRowCount(0)
            self.set_table_content()
        else: # 如果没有被选中的记录
            QMessageBox.warning(self,'Prompt','Please select', QMessageBox.Ok)

    def quit(self):
        self.close()

    # 取消这条记录，表示银行拒绝认证
    def reject(self):
        global client, contract_abi, to_address
        if self.table.selectionModel().hasSelection():
            row = self.table.currentRow()
            args = [self.table.item(row, 0).text(), self.table.item(row, 1).text(), \
                 int(self.table.item(row, 2).text()), self.table.item(row, 4).text()]
            print(args)
            # 调用合约函数 remove ，移除这条记录
            result = client.sendRawTransactionGetReceipt(to_address, contract_abi, "remove", args)
            print("receipt:",result)
            QMessageBox.information(self,'Prompt','success', QMessageBox.Ok)
            self.table.setRowCount(0)
            self.set_table_content()
        else:
            QMessageBox.warning(self,'Prompt','Please select', QMessageBox.Ok)

# 定义 Companies 类
class Companies(QMainWindow, Ui_Companies):
    def __init__(self, parent=None):
        super(Companies, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Company")
        # 设置交易信息列表表头
        self.headers = ['From','To','Amount','Status','Due date']
        self.table_info_bor.setColumnCount(5) 
        self.table_info_bor.setHorizontalHeaderLabels(self.headers)

        self.table_info_lent.setColumnCount(5) 
        self.table_info_lent.setHorizontalHeaderLabels(self.headers)

        self.table_trans_bor.setColumnCount(5)
        self.table_trans_bor.setHorizontalHeaderLabels(self.headers)

        self.table_trans_lent.setColumnCount(5)
        self.table_trans_lent.setHorizontalHeaderLabels(self.headers)

        self.table_repay.setColumnCount(5)   
        self.table_repay.setHorizontalHeaderLabels(self.headers)
        self.btn_quit.clicked.connect(self.quit)
        self.btn_reset_trans.clicked.connect(self.reset_transfer)
        self.btn_submit_trans.clicked.connect(self.submit_transfer)
        self.btn_reset_fin.clicked.connect(self.reset_finance)
        self.btn_submit_fin.clicked.connect(self.submit_finance)
        self.btn_reset_pur.clicked.connect(self.reset_purchase)
        self.btn_submit_pur.clicked.connect(self.submit_purchase)
        self.btn_ok_repay.clicked.connect(self.repay)

        self.btn_transfer.clicked.connect(self.transfer_view)
        self.btn_purchase.clicked.connect(self.purchase_view)
        self.btn_finance.clicked.connect(self.finance_view)
        self.btn_info.clicked.connect(self.info_view)
        self.btn_repay.clicked.connect(self.repay_view)

        self.table_info_bor.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_info_lent.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_trans_bor.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.table_trans_lent.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)

    # 基本信息
    def set_basic_info(self, name):
        global client, contract_abi, to_address
   
        self.table_info_bor.setRowCount(0)
        self.table_info_lent.setRowCount(0)
        self.table_trans_bor.setRowCount(0)
        self.table_trans_lent.setRowCount(0)
        self.table_repay.setRowCount(0)
        self.set_table_info_bor_content(name)
        self.set_table_info_lent_content(name)
        self.set_table_trans_bor_content(name) 
        self.set_table_trans_lent_content(name)
        self.set_table_repay_content(name)
        self.company_name = name
        self.total_borrowed = 0
        self.total_lent = 0
        for i in range(self.table_info_bor.rowCount()):
            self.total_borrowed += int(self.table_info_bor.item(i,2).text())
        for i in range(self.table_info_lent.rowCount()):
            self.total_lent += int(self.table_info_lent.item(i,2).text())
        self.line_basic_borr.setText(str(self.total_borrowed))
        self.line_basic_lent.setText(str(self.total_lent))
        self.transfer_date.setDateTime(QDateTime.currentDateTime())
        self.finance_date.setDateTime(QDateTime.currentDateTime())
        self.purchase_date.setDateTime(QDateTime.currentDateTime())

    # 定义显示基本信息时的borrow信息显示列表形式
    def set_table_info_bor_content(self,name):
        global client, contract_abi, to_address
        # 调用合约函数 selectFromReceipt ，返回信息元组
        result = client.call(to_address, contract_abi, "selectFromReceipt", [name, 1])
        # 在终端输出，便于调试
        print("receipt:",result)
        # 显示信息
        row_lenth = len(result[0])
        for i in range(row_lenth):
            row = self.table_info_bor.rowCount()
            self.table_info_bor.setRowCount(row + 1)
            self.table_info_bor.setItem(row,0,QTableWidgetItem(result[1][i]))
            self.table_info_bor.setItem(row,1,QTableWidgetItem(result[0][i]))
            self.table_info_bor.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table_info_bor.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table_info_bor.setItem(row,4,QTableWidgetItem(result[4][i]))

    # 定义显示基本信息时的lent信息显示列表形式
    def set_table_info_lent_content(self,name):
        global client, contract_abi, to_address
        # 调用合约函数 selectFromReceipt ，返回信息元组
        result = client.call(to_address, contract_abi, "selectFromReceipt", [name, 0])
        # 在终端输出，便于调试
        print("receipt:",result)
        # 显示信息
        row_lenth = len(result[0])
        for i in range(row_lenth):
            row = self.table_info_lent.rowCount()
            self.table_info_lent.setRowCount(row + 1)
            self.table_info_lent.setItem(row,0,QTableWidgetItem(result[1][i]))
            self.table_info_lent.setItem(row,1,QTableWidgetItem(result[0][i]))
            self.table_info_lent.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table_info_lent.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table_info_lent.setItem(row,4,QTableWidgetItem(result[4][i]))

    # 定义transfer时的borrow信息显示列表形式
    def set_table_trans_bor_content(self,name):
        global client, contract_abi, to_address
        # 调用合约函数 selectFromReceipt ，返回信息元组
        result = client.call(to_address, contract_abi, "selectFromReceipt", [name, 1])
        # 在终端输出，便于调试
        print("receipt:",result)
        # 显示信息
        row_lenth = len(result[0])
        for i in range(row_lenth):
            row = self.table_trans_bor.rowCount()
            self.table_trans_bor.setRowCount(row + 1)
            self.table_trans_bor.setItem(row,0,QTableWidgetItem(result[1][i]))
            self.table_trans_bor.setItem(row,1,QTableWidgetItem(result[0][i]))
            self.table_trans_bor.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table_trans_bor.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table_trans_bor.setItem(row,4,QTableWidgetItem(result[4][i]))

    # 定义transfer时的lent信息显示列表形式
    def set_table_trans_lent_content(self,name):
        global client, contract_abi, to_address
        # 调用合约函数 selectFromReceipt，返回信息元组
        result = client.call(to_address, contract_abi, "selectFromReceipt", [name, 0])
        # 在终端输出，便于调试
        print("receipt:",result)
        row_lenth = len(result[0])
        # 显示信息
        for i in range(row_lenth):
            row = self.table_trans_lent.rowCount()
            self.table_trans_lent.setRowCount(row + 1)
            self.table_trans_lent.setItem(row,0,QTableWidgetItem(result[1][i]))
            self.table_trans_lent.setItem(row,1,QTableWidgetItem(result[0][i]))
            self.table_trans_lent.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table_trans_lent.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table_trans_lent.setItem(row,4,QTableWidgetItem(result[4][i]))
    

    # 定义在repay时输出的显示列表形式
    def set_table_repay_content(self,name):
        global client, contract_abi, to_address
        # 调用合约函数 selectFromReceipt，返回信息元组
        result = client.call(to_address, contract_abi, "selectFromReceipt", [name, 1])
        # 在终端输出，便于调试
        print("receipt:",result)
        # 显示信息
        row_lenth = len(result[0])
        for i in range(row_lenth):
            row = self.table_repay.rowCount()
            self.table_repay.setRowCount(row + 1)
            self.table_repay.setItem(row,0,QTableWidgetItem(result[0][i]))
            self.table_repay.setItem(row,1,QTableWidgetItem(result[1][i]))
            self.table_repay.setItem(row,2,QTableWidgetItem(str(result[2][i])))
            self.table_repay.setItem(row,3,QTableWidgetItem(result[3][i]))
            self.table_repay.setItem(row,4,QTableWidgetItem(result[4][i]))  
       
    def info_view(self):
        self.stackedWidget.setCurrentIndex(0)
        self.set_basic_info(self.company_name)
    def transfer_view(self):
        self.stackedWidget.setCurrentIndex(1)
        self.set_basic_info(self.company_name)
    def purchase_view(self):
        self.stackedWidget.setCurrentIndex(2)
    def finance_view(self):
        self.stackedWidget.setCurrentIndex(3)     
    def repay_view(self):
        self.stackedWidget.setCurrentIndex(4)
        self.set_basic_info(self.company_name)

    def quit(self):
        self.close()

    # 重置transfer的输入框
    def reset_transfer(self):
        self.line_trans_from.clear()
        self.line_trans_to.clear()
        self.line_trans_amt.clear()

    # 提交transfer设置内容
    def submit_transfer(self):
        global client, contract_abi, to_address
        if self.table_trans_lent.selectionModel().hasSelection() and self.table_trans_bor.selectionModel().hasSelection():
            row_lent = self.table_trans_lent.currentRow()
            row_bor = self.table_trans_bor.currentRow()
            args = [self.table_trans_lent.item(row_lent, 1).text(), self.company_name, self.table_trans_bor.item(row_bor, 0).text(), int(self.line_trans_amt.text())]
            print(args) # 在终端输出，便于调试
            if self.table_trans_bor.item(row_bor, 3).text() == "authorized" and self.table_trans_lent.item(row_lent, 3).text() == "authorized":
                result = client.sendRawTransactionGetReceipt(to_address, contract_abi, "transfer", args)
                print("receipt:",result['output'])
                # 由于难以找到bug，所以这一功能暂时只能在链端用命令实现
                QMessageBox.information(self,'Prompt','Fail', QMessageBox.Ok)
             
            else:
                QMessageBox.warning(self,'Error','Please check', QMessageBox.Ok)
        else:
            QMessageBox.warning(self,'Prompt','Please select', QMessageBox.Ok)
        
    # 重置finance的输入框
    def reset_finance(self):
        self.line_fin_amt.clear()

    # 提交融资设置
    def submit_finance(self):
        _amt = int(self.line_fin_amt.text())
        _due = self.finance_date.dateTime().toString("yyyy/MM/dd hh:mm:ss")
        if _amt > (self.total_lent - self.total_borrowed):
            QMessageBox.warning(self,'Error',"failed with {}.".format(str(self.total_lent - self.total_borrowed)), QMessageBox.Ok)
        else:
            global client, contract_abi, to_address
            args = [self.company_name, _amt,_due]
            client.sendRawTransactionGetReceipt(to_address, contract_abi, "finance", args)
            QMessageBox.information(self,'Prompt','success。', QMessageBox.Ok)

    # 重置purchase的输入框
    def reset_purchase(self):
        self.line_pur_amt.clear()
        self.line_pur_from.clear()

    # 提交purchase设置
    def submit_purchase(self):    
        global client, contract_abi, to_address
        args = [self.line_pur_from.text(), self.company_name , int(self.line_pur_amt.text()), self.purchase_date.dateTime().toString("yyyy/MM/dd hh:mm:ss")]
        client.sendRawTransactionGetReceipt(to_address, contract_abi, "purchase", args)
        QMessageBox.information(self,'Prompt','success。', QMessageBox.Ok)

    # 还款
    def repay(self):
        global client, contract_abi, to_address
        if self.table_repay.selectionModel().hasSelection():
            row = self.table_repay.currentRow()
            args = [self.table_repay.item(row, 0).text(), self.table_repay.item(row, 1).text(), \
                 int(self.table_repay.item(row, 2).text()),self.table_repay.item(row, 4).text()]
            print(args)
            if self.table_repay.item(row, 3).text() == "authorized":
                # 调用智能合约中的repay函数，并返回结果
                result = client.sendRawTransactionGetReceipt(to_address, contract_abi, "repay", args)
                print("receipt:",result)
                res = hex_to_signed(result['output'])
                if res == 0:
                        QMessageBox.information(self,'Prompt','success。', QMessageBox.Ok)
                else:
                        QMessageBox.warning(self,'Prompt','fail。', QMessageBox.Ok)                        
                self.table_repay.setRowCount(0)
                self.set_table_repay_content(self.company_name)
            else:
                QMessageBox.warning(self,'Error','请先认证相关交易。', QMessageBox.Ok)
        else:
            QMessageBox.warning(self,'Prompt','请先选择相关记录。', QMessageBox.Ok)

class Signup(QMainWindow, Ui_Signup):
    def __init__(self, parent=None):
        super(Signup, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Sign Up")
        self.btn_register.clicked.connect(self.press_register)
        self.btn_quit.clicked.connect(self.close)

	# 注册
    def press_register(self):
        name, password, balance = self.line_name.text(), self.line_pwd.text(), self.line_balance.text()
        # balabce代表启动资金
        balance = int(balance)
        if len(name) > 256:
            QMessageBox.warning(self, 'Error', '名称过长。')
            sys.exit(1)
        print("starting : {} {} ".format(name, password))
        ac = Account.create(password)
        print("new address :\t", ac.address)
        print("new privkey :\t", encode_hex(ac.key))
        print("new pubkey :\t", ac.publickey)

        kf = Account.encrypt(ac.privateKey, password)
        keyfile = "{}/{}.keystore".format(client_config.account_keyfile_path, name)
        print("save to file : [{}]".format(keyfile))
        with open(keyfile, "w") as dump_f:
            json.dump(kf, dump_f)
            dump_f.close()
        print(
            "INFO >> Read [{}] again after new account,address & keys in file:".format(keyfile))
        with open(keyfile, "r") as dump_f:
            keytext = json.load(dump_f)
            privkey = Account.decrypt(keytext, password)
            ac2 = Account.from_key(privkey)
            print("address:\t", ac2.address)
            print("privkey:\t", encode_hex(ac2.key))
            print("pubkey :\t", ac2.publickey)
            print("\naccount store in file: [{}]".format(keyfile))
            dump_f.close()

        global client, contract_abi, to_address
        args = [name, ac.address, 'Company', balance]
        # 调用智能合约中的register函数    
        receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"register",args)
        print("receipt:",receipt['output'])

        QMessageBox.information(self,'Prompt','success。', QMessageBox.Ok)

class Login(QMainWindow, Ui_Login):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.setupUi(self)
        self.setWindowTitle("Log In")
        self.btn_login.clicked.connect(self.validate)
        self.btn_signup.clicked.connect(self.press_signup)

    def validate(self):
        name = self.line_name.text()
        password = self.line_pwd.text()
        if name == "bank" and password == "bank":
            bank_window.show()
            bank_window.set_table_content()
        else:
            keyfile = "{}/{}.keystore".format(client_config.account_keyfile_path, name)
            # 如果名字不存在
            if os.path.exists(keyfile) is False:
                QMessageBox.warning(self,
                        "error",
                        "名称 {} 不存在，请先注册。".format(name),
                        QMessageBox.Yes)
            else:
                print("name : {}, keyfile:{} ,password {}  ".format(name, keyfile, password))
                try:
                    with open(keyfile, "r") as dump_f:
                        keytext = json.load(dump_f)
                        privkey = Account.decrypt(keytext, password)
                        ac2 = Account.from_key(privkey)
                        print("address:\t", ac2.address)
                        print("privkey:\t", encode_hex(ac2.key))
                        print("pubkey :\t", ac2.publickey)
                        company_window.show()
                        company_window.set_basic_info(name)
                except Exception as e:
                    QMessageBox.warning(self,
                            "error",
                            ("Failed to load account info for [{}],"
                                            " error info: {}!").format(name, e),
                            QMessageBox.Yes)

    def press_signup(self):
        signup_window.show()


if __name__ == "__main__":
    # 指定智能合约地址
    abi_file = "contracts/myContract.abi"
    data_parser = DatatypeParser()
    data_parser.load_abi_file(abi_file)
    contract_abi = data_parser.contract_abi
    client = BcosClient()
    # init中输出的地址
    to_address = '0x4fb700f036dbd8a80940a88df8d9e55705a8ac97'

    app = QtWidgets.QApplication(sys.argv)
    login_window = Login()
    signup_window = Signup()
    bank_window = Bank()
    company_window = Companies()
    login_window.show()
    app.exec_()
    client.finish()
