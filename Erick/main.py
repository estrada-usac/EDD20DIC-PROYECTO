from BD import *

# Lista De BD
repo_BD = DB()

# Nueva BD
repo_BD.createDatabase("Data_Base1")
repo_BD.createDatabase("Data_Base2")
repo_BD.createDatabase("Data_Base3")
repo_BD.createDatabase("Data_Base5")

repo_BD.alterDatabase("Data_Base5","Data_Base4")
repo_BD.dropDatabase("Data_Base3")

# Ver Lista De BD
print(repo_BD.showDatabases())
