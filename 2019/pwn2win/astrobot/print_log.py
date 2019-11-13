# -*- coding: utf-8 -*-

# Copyright © 2019 MV9rwGOf08 team
# Redistribution and use in source and binary forms, with or without
# modification, are permitted.

from __future__ import unicode_literals

import pyte
import re

wh = (40, 17)

screen = pyte.Screen(*wh)
stream = pyte.Stream(screen)

def draw(inp):
    for l in inp:
        if 'direction' in l:
            m = re.search('direction: (.*)\n', l)
            print 'direction:', m.group(1)
            l = re.sub('direction:.*\n', '', l)
        stream.feed(l)
    for l in screen.display:
        print l.encode('utf-8')

a = []
with open('ab.log') as f:
    for l in f:
        # print repr(l)
        l = l.decode('utf-8')
        # TODO: It looses the bottom line in every screen.
        if u'┌[' in l:
            draw(a)
            a = []
        a.append(l)
    draw(a)

print
