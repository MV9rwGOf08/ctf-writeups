# -*- coding: utf-8 -*-

# Copyright © 2018 MV9rwGOf08 team
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

import sys
import os
import fcntl
import time
import subprocess
import re
import os.path
import ast
import random

p = subprocess.Popen(r'SSH_ASKPASS="./t.sh" DISPLAY=:0 setsid -w ssh -t -t sgle@10.133.70.3',
                    shell = True,
                    stdin = subprocess.PIPE,
                    stdout = subprocess.PIPE,
                    # stderr = subprocess.STDOUT
                    )

fd = p.stdout.fileno()
fl = fcntl.fcntl(fd, fcntl.F_GETFL)
fcntl.fcntl(fd, fcntl.F_SETFL, fl | os.O_NONBLOCK)

i1 = '\033OC'
i2 = '\033OD'

best_progress = 0

new_best = []

reset = random.randint(1, 15)
# reset = random.randint(1, 8)
best = []
if os.path.exists('best'):
    with open('best') as f:
        best_progress, best = ast.literal_eval(f.read())
        if len(best) > reset:
            best = best[ : -reset]
        else:
            best = []

with open('out', 'w') as f:
    while True:
        try:
            i = p.stdout.read(4096)
        except IOError:
            continue
        f.write('{} {}\n'.format(time.time(), repr(i)))
        f.flush()
        if 'CTF-BR' in i:
            os.system('cp out out.flag')
        #sys.stdout.write(i)
        #sys.stdout.flush()
        if 'X' in i:
            break
        t = re.findall(r'(\[\d+:\d+\]).*(\[\d+.\d+\])', i)
        if t:
            c = t[0][0]
            progress = float(t[0][1].strip('[]'))
            if progress > 137:
                os.system('cp out out.flag2')
            move = None
            if best:
                if best[0][0] == c and abs(progress - best[0][2]) < 0.2:
                    move = best[0][1]
                    best.pop(0)
            else:
                move = random.choice([ i1, i2 ] + [ None ] * 20)
            if move:
                new_best.append((c, move, progress))
                p.stdin.write(move)
                p.stdin.flush()
        print >>f, t

os.system('cp out out.`date +%s`')
print progress
if progress > best_progress:
    with open('best', 'w') as f:
        f.write(repr([ progress, new_best ]))

p.terminate()
p.kill()
