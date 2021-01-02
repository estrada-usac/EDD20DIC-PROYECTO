import storageManager

storageManager.createDatabase("database1", "avl", "utf8")
storageManager.createDatabase("database2", "b", "utf8")
storageManager.createDatabase("database3", "bplus", "utf8")
storageManager.createDatabase("database4", "hash", "utf8")
storageManager.createDatabase("database5", "isam", "utf8")
storageManager.createDatabase("database6", "dict", "utf8")
storageManager.createDatabase("database7", "json", "utf8")

storageManager.createTable("database1", "table1", 3)

storageManager.createTable("database2", "table1", 3)
storageManager.createTable("database2", "table2", 3)

storageManager.createTable("database3", "table1", 3)
storageManager.createTable("database3", "table2", 3)
storageManager.createTable("database3", "table3", 3)

storageManager.createTable("database4", "table1", 3)
storageManager.createTable("database4", "table2", 3)
storageManager.createTable("database4", "table3", 3)
storageManager.createTable("database4", "table4", 3)

storageManager.createTable("database5", "table1", 3)
storageManager.createTable("database5", "table2", 3)
storageManager.createTable("database5", "table3", 3)
storageManager.createTable("database5", "table4", 3)
storageManager.createTable("database5", "table5", 3)

storageManager.createTable("database6", "table1", 3)
storageManager.createTable("database6", "table2", 3)
storageManager.createTable("database6", "table3", 3)
storageManager.createTable("database6", "table4", 3)
storageManager.createTable("database6", "table5", 3)
storageManager.createTable("database6", "table6", 3)

storageManager.createTable("database7", "table1", 3)
storageManager.createTable("database7", "table2", 3)
storageManager.createTable("database7", "table3", 3)
storageManager.createTable("database7", "table4", 3)
storageManager.createTable("database7", "table5", 3)
storageManager.createTable("database7", "table6", 3)
storageManager.createTable("database7", "table7", 3)