# -*- coding: utf-8 -*- 
import os,sys,json,glob
from client.contractnote import ContractNote
from client.bcosclient import BcosClient
from client.datatype_parser import DatatypeParser
from client.common.compiler import Compiler
from client.bcoserror import BcosException, BcosError
from client_config import client_config
from eth_utils import to_checksum_address
from eth_utils.hexadecimal import encode_hex
from eth_account.account import Account

client = BcosClient()

# 设定abi文件
if os.path.isfile(client_config.solc_path) or os.path.isfile(client_config.solcjs_path):
    Compiler.compile_file("contracts/myContract.sol")
abi_file = "contracts/myContract.abi"
data_parser = DatatypeParser()
data_parser.load_abi_file(abi_file)
contract_abi = data_parser.contract_abi

# 部署智能合约
with open("contracts/myContract.bin", 'r') as load_f:
    contract_bin = load_f.read()
    load_f.close()
result = client.deploy(contract_bin)
print("deploy",result)
print("new address : ",result["contractAddress"])
contract_name =  os.path.splitext(os.path.basename(abi_file))[0]
memo = "tx:"+result["transactionHash"]

# 部署结果存入文件
from client.contractnote import ContractNote
ContractNote.save_history(contract_name, result["contractAddress"], int(result["blockNumber"], 16), memo)

# 创建company_table，receipt_table
to_address = result['contractAddress'] 
receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"createCompanyTable")
if receipt['output'] != 0:
    print("company_table already exists.")
else: print("create company_table successfully.")
receipt = client.sendRawTransactionGetReceipt(to_address,contract_abi,"createReceiptTable")
if receipt['output'] != 0:
    print("receipt_table already exists.")
else: print("create receipt_table successfully.")
