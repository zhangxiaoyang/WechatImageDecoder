#!/usr/bin/env python
# zhangxiaoyang.hit[at]gmail.com

import re

class WechatImageDecoder:
    def __init__(self, datfile):
        datfile = datfile.lower()

        decoder = self._match_decoder(datfile)
        decoder(datfile)

    def _match_decoder(self, datfile):
        decoders = {
            r'.+\.dat$': self._decode_pc_dat,
            r'cache\.data\.\d+$': self._decode_android_dat,
            None: self._decode_unknown_dat,
        }

        for k, v in decoders.iteritems():
            if k is not None and re.match(k, datfile):
                return v
        return decoders[None]

    def _decode_pc_dat(self, datfile):
        magic = 0x51

        with open(datfile, 'rb') as f:
            buf = bytearray(f.read())

        imgfile = re.sub(r'.dat$', '.jpg', datfile)
        with open(imgfile, 'wb') as f:
            newbuf = bytearray(map(lambda b: b ^ magic, list(buf)))
            f.write(str(newbuf))

    def _decode_android_dat(self, datfile):
        with open(datfile, 'rb') as f:
            buf = f.read()

        last_index = 0
        for i, m in enumerate(re.finditer(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', buf)):
            if m.start() == 0:
                continue

            imgfile = '%s_%d.jpg' % (datfile, i)
            with open(imgfile, 'wb') as f:
                f.write(buf[last_index: m.start()])
            last_index = m.start()

    def _decode_unknown_dat(self, datfile):
        raise Exception('Unknown file type')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print '\n'.join([
            'Usage:',
            '  python WechatImageDecoder.py [datfile]',
            '',
            'Example:',
            '  # PC:',
            '  python WechatImageDecoder.py 1234567890.dat',
            '',
            '  # Android:',
            '  python WechatImageDecoder.py cache.data.10'
        ])
        sys.exit(1)

    _,  datfile = sys.argv[:2]
    try:
        WechatImageDecoder(datfile)
    except Exception as e:
        print e
        sys.exit(1)
    sys.exit(0)
