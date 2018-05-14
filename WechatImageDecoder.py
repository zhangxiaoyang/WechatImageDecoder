#!/usr/bin/env python
# zhangxiaoyang.hit[at]gmail.com

import re

class WechatImageDecoder:
    def __init__(self, *args):
        datfile = args[0]
        decoder = self._match_decoder(datfile)
        decoder(*args)

    def _match_decoder(self, datfile):
        decoders = {
            r'.+\.dat$': self._decode_pc_dat,
            r'cache\.data\.\d+$': self._decode_android_dat,
            None: self._decode_unknown_dat,
        }

        for k, v in decoders.items():
            if k is not None and re.match(k, datfile.lower()):
                return v
        return decoders[None]

    def _decode_pc_dat(self, datfile, filetype):
        header_map = {
            'jpg': 0xff,
            'png': 0x89,
            'gif': 0x47,
        }
        filetype = filetype.lower()
        if filetype not in header_map:
            filetype = 'jpg'
        header_code = header_map[filetype]

        with open(datfile, 'rb') as f:
            buf = bytearray(f.read())
        magic = header_code ^ list(buf)[0] if buf else 0x00
        imgfile = re.sub(r'.dat$', '.' + filetype, datfile)
        with open(imgfile, 'wb') as f:
            newbuf = bytearray([b ^ magic for b in list(buf)])
            f.write(newbuf)

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
    if len(sys.argv) < 2:
        print('\n'.join([
            'Usage:',
            '  python WechatImageDecoder.py [datfile] [jpg|png|gif]',
            '',
            'Example:',
            '  # PC:',
            '  python WechatImageDecoder.py 1234567890.dat jpg',
            '',
            '  # Android:',
            '  python WechatImageDecoder.py cache.data.10'
        ]))
        sys.exit(1)

    _,  datfile, filetype = sys.argv[:2] + [sys.argv[2] if len(sys.argv) > 2 else 'jpg']
    try:
        WechatImageDecoder(datfile, filetype)
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)
