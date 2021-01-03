import hashlib

m = hashlib.md5()
#m.update(b"Nobody inspects")
#m.update(b" the spammish repetition")
h = bytes('hola', encoding="utf-8")
m.update(h)
print(m.digest())
print(m.digest_size)
print(m.block_size)
print(m.hexdigest())

a = hashlib.md5(b"hola").hexdigest()
print(a)
