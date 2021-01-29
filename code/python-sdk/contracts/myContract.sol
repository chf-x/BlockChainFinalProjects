pragma solidity ^0.4.24;
pragma experimental ABIEncoderV2;

import "./Table.sol";

contract myAsset {
    // event
    event RegisterEvent(int256 ret, string account, int256 asset_value);
    event TransferEvent(int256 ret, string from_account, string to_account, int256 amount);
    event issueReceivablesEvent(int256 ret, string id, string acc1, string acc2, int256 money);
    event payReceivablesEvent(int256 ret, string id, int256 money);
    event transferReceivablesEvent(int256 ret, string old_id, string new_id, string acc);

    constructor() public {
        // 构造函数中创建t_asset表
        createTable();
    }

    function createTable() private {
        TableFactory tf = TableFactory(0x1001);
        // 资产管理表, key : account, field : asset_value
        // |   资产账户(主键)      |     信用额度       |
        // |-------------------- |-------------------|
        // |        account      |    asset_value    |
        // |---------------------|-------------------|
        //
        // 创建表
        tf.createTable("t_asset", "account", "asset_value");
        // 交易记录表, key: id, field: acc1, acc2, money, status
        // | 交易单号(key) | 债主 | 借债人 | 债务金额 |   状态   |
        // |-------------|------|-------|---------|---------|
        // |     id      | acc1 | acc2  |  money  | status  |
        // |-------------|------|-------|---------|---------|
        tf.createTable("t_transaction", "id","acc1, acc2, money, status");
    }

    // 返回t_asset
    function openAssetTable() private returns(Table) {
        TableFactory tf = TableFactory(0x1001);
        Table table = tf.openTable("t_asset");
        return table;
    }

    // 返回t_transaction
    function openTransactionTable() private returns(Table) {
        TableFactory tf = TableFactory(0x1001);
        Table table = tf.openTable("t_transaction");
        return table;
    }

    /*
    描述 : 根据资产账户查询信用金额
    参数 ： 
            account : 资产账户
    返回值：
            参数一： 成功返回0, 账户不存在返回-1
            参数二： 第一个参数为0时有效，信用金额
    */
    function select(string account) public constant returns(int256, int256) {
        // 打开表
        Table table = openAssetTable();
        // 查询
        Entries entries = table.select(account, table.newCondition());
        int256 asset_value = 0;
        if (0 == uint256(entries.size())) {
            return (-1, asset_value);
        } else {
            Entry entry = entries.get(0);
            return (0, int256(entry.getInt("asset_value")));
        }
    }

    /*
    描述 : 根据id查询交易
    参数 ： 
            id : 交易ID
    返回值：
            参数一： 成功则数组的首个元素为0,；若成功,则第二个元素为初始欠条金额，第三个元素为欠条未还清的金额
            参数二： 若成功，则第一个元素为债主，第二个元素为欠款人
    */
    
    function select_transaction(string id) public constant returns(int256[], bytes32[]) {
        // 打开表
        Table table = openTransactionTable();
        // 查询
        Entries entries = table.select(id, table.newCondition());
        //         bytes32[] memory str_list = new bytes32[](2);

        int256[] memory int_list = new int256[](3);   //ret_code, money, status
        bytes32[] memory str_list = new bytes32[](2);   //acc1, acc2
        if (0 == uint256(entries.size())) {
            int_list[0] = -1;
            return (int_list, str_list);
        } else {
            Entry entry = entries.get(0);
            int_list[1] = entry.getInt("money");
            int_list[2] = entry.getInt("status");
            str_list[0] = entry.getBytes32("acc1");
            str_list[1] = entry.getBytes32("acc2");
            return (int_list, str_list);
        }
    }

    /*
    描述 : 资产注册
    参数 ： 
            account : 资产账户
            amount  : 信用额度
    返回值：
            0  资产注册成功
            -1 资产账户已存在
            -2 其他错误
    */
    function register(string account, int256 asset_value) public returns(int256){
        int256 ret_code = 0;
        int256 ret = 0;
        int256 temp_asset_value = 0;
        // 查询账户是否存在
        (ret, temp_asset_value) = select(account);
        if(ret != 0) {
            Table table = openAssetTable();
            
            Entry entry = table.newEntry();
            entry.set("account", account);
            entry.set("asset_value", int256(asset_value));
            // 插入
            int count = table.insert(account, entry);
            if (count == 1) {
                // 成功
                ret_code = 0;
            } else {
                // 失败? 无权限或者其他错误
                ret_code = -2;
            }
        } else {
            // 账户已存在
            ret_code = -1;
        }

        emit RegisterEvent(ret_code, account, asset_value);

        return ret_code;
    }

    /*
    描述 : 添加交易记录（打欠条）
    参数 ： 
            id : 交易编号
            acc1 : 债主
            acc2 : 借债人
            money: 初始金额 （欠条未还清的金额与初始金额一致）
    返回值：
            0  交易添加成功
            -1 交易ID已存在
            -2 其他错误
            -3 信用额度转让失败
    */
    function issueReceivables(string id, string acc1, string acc2, int256 money) public returns(int256){
        int256 ret = 0;
        bytes32[] memory str_list = new bytes32[](2);
        int256[] memory int_list = new int256[](3);
        

        Table table = openTransactionTable();

        Entry entry0 = table.newEntry();
        entry0.set("id", id);
        entry0.set("acc1", acc1);
        entry0.set("acc2", acc2);
        entry0.set("money", int256(money));
        entry0.set("status", int256(money));
        // 插入
        int count = table.insert(id, entry0);

        emit issueReceivablesEvent(ret, id, acc1, acc2, money);

        return ret;
    }

    /*
    描述 : 更新交易记录(支付欠条)
    参数 ： 
            id : 交易编号
            money: 金额
    返回值：
             0  交易更新成功
            -1 交易ID不存在
            -2 还债金额大于债款
            -3 其他错误
            -4 信用返还有问题
    */
    function payReceivables(string id, int256 money) public returns(int256, string[]){
        int256 ret_code = 0;
        bytes32[] memory str_list = new bytes32[](2);
        int256[] memory int_list = new int256[](3);
        string[] memory acc_list = new string[](2);
        (int_list, str_list) = select_transaction(id);
        acc_list[0] = byte32ToString(str_list[0]);
        acc_list[1] = byte32ToString(str_list[1]);

        if(int_list[0] == 0) {

            Table table = openTransactionTable();

            Entry entry0 = table.newEntry();
            entry0.set("id", id);
            entry0.set("acc1", byte32ToString(str_list[0]));
            entry0.set("acc2", byte32ToString(str_list[1]));
            entry0.set("money", int_list[1]);
            entry0.set("status", (int_list[2] - money));

            int count = table.update(id, entry0, table.newCondition());
            if(count != 1) {
                ret_code = -3;
                emit payReceivablesEvent(ret_code, id, money);
                return (ret_code,acc_list);
            }

            int256 temp = transfer(byte32ToString(str_list[0]),byte32ToString(str_list[1]),money);
            if(temp != 0){
                ret_code = -4 * 10 + temp;
                emit payReceivablesEvent(ret_code, id, money);
                return (ret_code,acc_list);
            }

            ret_code = 0;
      
        } else { 
            ret_code = -1;
        }
        emit payReceivablesEvent(ret_code, id, money);

        return (ret_code,acc_list);
    }

    /*
    描述 ： 转让应收账款
    参数 ：
            old_id: 需要拆分的欠条id
            new_id: 新创建的欠条的id
            acc: 新创建欠条的债主
            money: 欠条拆分的金额
    返回值 :
             0 欠条拆分成功
            -1 拆分的欠条id不存在
            -2 用户acc不存在
            -3 新欠条创建不成功
    */
    function transferReceivables(string old_id, string new_id, string acc) public returns(int256) {
        int256 ret_code = 0;
        int256 ret = 0;
        int temp = 0;
        bytes32[] memory str_list = new bytes32[](2);
        int256[] memory int_list = new int256[](3);
        string[] memory acc_list = new string[](2);
        // 查询该欠条是否存在
        (int_list, str_list) = select_transaction(old_id);

        if(int_list[0] == 0) {
            // acc不存在
            (ret, temp) = select(acc);
            if(ret != 0) {
                ret_code = -5;
                emit transferReceivablesEvent(ret_code, old_id, new_id, acc);
                return ret_code;
            }

            // acc1先“还钱”给acc2，然后acc2再“借钱”给acc
            (ret,acc_list) = payReceivables(old_id, int_list[1]);
            if (ret != 0) {
                ret_code = -4;
                emit transferReceivablesEvent(ret_code, old_id, new_id, acc);
                return ret_code;
            }
            transfer(acc,byte32ToString(str_list[1]),int_list[1]);
            transfer(byte32ToString(str_list[1]),byte32ToString(str_list[0]),int_list[1]);
            ret = issueReceivables(new_id, byte32ToString(str_list[0]), acc, int_list[1]);
            if (ret != 0) {
                ret_code = -3;
                emit transferReceivablesEvent(ret_code, old_id, new_id, acc);
                return ret_code;
            }

        } else {    // 拆分的欠条id不存在
            ret_code = -1;
        }

        emit transferReceivablesEvent(ret_code, old_id, new_id, acc);
        return ret_code;
    }

    function transfer(string from_account, string to_account, int256 amount) public returns(int256) {
        int ret_code = 0;
        int256 ret = 0;
        int256 from_asset_value = 0;
        int256 to_asset_value = 0;
        
        (ret, from_asset_value) = select(from_account);
        if(ret != 0) {
            ret_code = -1;
            // 转移账户不存在
            emit TransferEvent(ret_code, from_account, to_account, amount);
            return ret_code;

        }

        (ret, to_asset_value) = select(to_account);
        if(ret != 0) {
            ret_code = -2;
            emit TransferEvent(ret_code, from_account, to_account, amount);
            return ret_code;
        }

        if(from_asset_value < amount) {
            ret_code = -3;
            emit TransferEvent(ret_code, from_account, to_account, amount);
            return ret_code;
        } 

        if (to_asset_value + amount < to_asset_value) {
            ret_code = -4;
            emit TransferEvent(ret_code, from_account, to_account, amount);
            return ret_code;
        }

        Table table = openAssetTable();

        Entry entry0 = table.newEntry();
        entry0.set("account", from_account);
        entry0.set("asset_value", int256(from_asset_value - amount));
        int count = table.update(from_account, entry0, table.newCondition());
        if(count != 1) {
            ret_code = -5;
            emit TransferEvent(ret_code, from_account, to_account, amount);
            return ret_code;
        }

        Entry entry1 = table.newEntry();
        entry1.set("account", to_account);
        entry1.set("asset_value", int256(to_asset_value + amount));
        table.update(to_account, entry1, table.newCondition());

        emit TransferEvent(ret_code, from_account, to_account, amount);

        return ret_code;
    }


    function byte32ToString(bytes32 x) public constant returns (string) {
       
       bytes memory bytesString = new bytes(32);
        uint charCount = 0;
        for (uint j = 0; j < 32; j++) {
            byte char = byte(bytes32(uint(x) * 2 ** (8 * j)));
            if (char != 0) {
                bytesString[charCount] = char;
                charCount++;
            }
        }
        bytes memory bytesStringTrimmed = new bytes(charCount);
        for (j = 0; j < charCount; j++) {
            bytesStringTrimmed[j] = bytesString[j];
        }
        return string(bytesStringTrimmed);
   }
}

