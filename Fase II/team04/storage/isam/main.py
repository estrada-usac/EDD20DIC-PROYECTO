import storage.isam.InterfazBD
import storage.isam.ISAMMode as Storage

vectorBases=Storage.showDatabases()
InterfazBD.PantallaBD(vectorBases)
