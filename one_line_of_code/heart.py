# -*- coding: utf-8 -*-

# % x, 0 <= x <= len(str)
print('\n'.join([''.join([('joyboy'[(x - y) % len('joyboy')] if ((x * 0.05) ** 2 + (y * 0.1) ** 2 - 1) ** 3 - (
        x * 0.05) ** 2 * (y * 0.1) ** 3 <= 0 else ' ') for x in range(-30, 30)]) for y in range(15, -15, -1)]))
