# -*- coding: utf-8 -*-

# Copyright © 2019 MV9rwGOf08 team
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

import os
os.environ['PWNLIB_NOTERM'] = '1'

from pwn import *
context.log_level = logging.CRITICAL
# autoflush
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)


# NOTE: 'screen' may be removed from cmd; horizontal line char would be 'u'.
os.system('killall screen')

# New York
cmd = 'TERM=xterm screen ssh -p2222 chall@142.93.190.87'

# Amsterdam
cmd = 'TERM=xterm screen ssh -p2222 chall@178.128.245.211'

# cmd = 'TERM=xterm screen ssh -v -p2222 chall@178.128.245.211'

cmd = 'TERM=xterm screen python astrobot.py'

p = process(cmd, shell = True, stdin = PTY)

f = open('ab.log', 'w')

# recvuntil() and log output into file
def ru(s, timeout = 10):
    t = p.recvuntil(s, timeout = timeout)
    f.write(t)
    return t

# ru(" password: ")
# p.sendline("eik7avou3yoo9Ohtai4a")

# p.interactive()
# exit()

ru("[")

right = '\033OC'
left = '\033OD'

# Commands:
# paragraph to reach the first star,
# paragraph to collect 1-7 stars, then the track repeats
# i - don't send anything, ignore event (used to hold queue)
# < - left arrow
# > - right arrow
# s> - sleep for 10ms, then send right arrow
# * - send space
# Each line: position/asterisks command
# NOTE: These commands depend on latency, because they should be sent
#       beforehand.

# Commands for ping ~45.7 ms:
t = '''
8/0 i
8/0 <
14/0 i
14/0 >

19/1 >
38/2 >
18/2 s>
8/3 >
13/3 <
4/4 >
34/4 <
19/4 >
31/5 i
31/5 s>
2/6 <
20/6 <
20/6 i
24/6 i
20/6 >
'''.strip()

# Command for local use with pipe:
t = '''
10/0 i
10/0 <
12/0 i
12/0 >

17/1 >
37/2 i
37/2 >
16/2 s>
6/3 >
15/3 <
2/4 >
36/4 <
19/4 s>
27/5 i
27/5 >
5/6 i
5/6 <
'''

# Populate commands up to 99 stars; i.e. (99/6 + 1) * 6, but we already have 6
p1, p2 = t.split('\n\n')
for i in range(99 / 6):
    p2 = re.sub(r'(\d+/)(\d+)',
                lambda m: m.group(1) + str(int(m.group(2)) + 6),
                p2)
    t += '\n' + p2

t = t.split('\n')

# queue of commands
q = []
for l in t:
    if l == '':
        continue
    a, b = l.split()
    q.append((a, b))

while True:
    t = ru('┌[', timeout = 0.5)
    if t == '':
        break
    t = ru(']────────')
    m = re.search(r':(\d+)](?:\xe2\x94\x80){2,3}\[\d+.\d\d(/\d+)\]', t)
    o = m.group(1) + m.group(2)
    pos = int(m.group(1))
    print '[' + t, '|{}{}{}|'.format(' ' * (pos - 1), 'V', ' ' * (38 - pos))
    if q and o == q[0][0]:
        d = q[0][1]
        q.pop(0)
        oo = 'direction: {} {}'.format(o, d)
        print oo
        f.write(oo + '\n')
        if re.match(r'^\*+$', d):
            p.send(' ' * len(d))
        elif d == 's>':
            time.sleep(0.01)
            p.send(right)
        elif d == '<':
            p.send(left)
        elif d == '>':
            p.send(right)
        elif d == 'i':
            print 'direction ignored'
        else:
            print 'wrong direction'

p.sendline('')

t = p.recvall()
f.write(t)

f.close()

# p.interactive()
