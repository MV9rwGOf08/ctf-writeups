# -*- coding: utf-8 -*-

# Copyright © 2018 MV9rwGOf08 team
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

import pexpect
import pexpect.ANSI
import ast

wh = (10, 50)

def to_matrix(inp):
    ansi = pexpect.ANSI.ANSI(*wh)
    ansi.write(inp)
    t = str(ansi)
    return map(list, t.split('\n'))

with open('out') as f:
    for l in f:
        if l.startswith("["):
            continue
        t, s = l.split(' ', 1)
        s = ast.literal_eval(s)
        m = to_matrix(s)
        for ll in m:
            print ''.join(ll)
        print
