#!/usr/bin/env python

class WechatImageDecoder:

    def __init__(self, datfile, imgfile):
        self._decode(datfile, imgfile)

    def _decode(self, datfile, imgfile):
        with open(datfile, 'rb') as f:
            buf = bytearray(f.read())

        with open(imgfile, 'wb') as f:
            newbuf = bytearray(map(lambda b: b^0x51, list(buf)))
            f.write(str(newbuf))

if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print '\n'.join([
            'Usage:',
            '  python WechatImageDecoder.py [datfile] [imgfile]',
            '',
            'Example:',
            '  python WechatImageDecoder.py 1145141041336905947.dat myimage.jpg'
        ])
        sys.exit(1)

    _,  datfile, imgfile = sys.argv[:3]
    WechatImageDecoder(datfile, imgfile)
    sys.exit(0)
