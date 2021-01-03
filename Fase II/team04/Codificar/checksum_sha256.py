import hashlib

m = hashlib.sha256()
m.update(b"Nobody inspects")
m.update(b" the spammish repetition")
m.digest()
m.digest_size
m.block_size
a = hashlib.sha256(b"hola").hexdigest()
print(a)