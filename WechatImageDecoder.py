#!/usr/bin/env python
# zhangxiaoyang.hit[at]gmail.com

import re
import os

def check_and_create_dir(file_path):
    dir = os.path.dirname(file_path)
    if not os.path.exists(dir):
        os.makedirs(dir)

class WechatImageDecoder:
    def __init__(self, dat_file,output_dir = "./"):
        self.output_dir = output_dir
        dat_file = dat_file.lower()

        decoder = self._match_decoder(dat_file)
        decoder(dat_file)

    def _match_decoder(self, dat_file):
        decoders = {
            r'.+\.dat$': self._decode_pc_dat,
            r'cache\.data\.\d+$': self._decode_android_dat,
            None: self._decode_unknown_dat,
        }

        for k, v in decoders.items():
            if k is not None and re.match(k, dat_file):
                return v
        return decoders[None]

    def _decode_pc_dat(self, dat_file):
        
        def do_magic(header_code, buf):
            return header_code ^ list(buf)[0] if buf else 0x00
        
        def decode(magic, buf):
            return bytearray([b ^ magic for b in list(buf)])
            
        def guess_encoding(buf):
            headers = {
                'jpg': (0xff, 0xd8),
                'png': (0x89, 0x50),
                'gif': (0x47, 0x49),
            }
            for encoding in headers:
                header_code, check_code = headers[encoding] 
                magic = do_magic(header_code, buf)
                _, code = decode(magic, buf[:2])
                if check_code == code:
                    return (encoding, magic)
            print('Decode failed')
            sys.exit(1) 

        with open(dat_file, 'rb') as f:
            buf = bytearray(f.read())
        file_type, magic = guess_encoding(buf)

        img_file = re.sub(r'.dat$', '.' + file_type, dat_file)
        fp = os.path.join(self.output_dir,img_file)
        check_and_create_dir(fp)
        with open(fp, 'wb') as f:
            new_buf = decode(magic, buf)
            f.write(new_buf)

    def _decode_android_dat(self, dat_file):
        with open(dat_file, 'rb') as f:
            buf = f.read()

        last_index = 0
        for i, m in enumerate(re.finditer(b'\xff\xd8\xff\xe0\x00\x10\x4a\x46', buf)):
            if m.start() == 0:
                continue

            imgfile = '%s_%d.jpg' % (dat_file, i)
            fp = os.path.join(self.output_dir,imgfile)
            check_and_create_dir(fp)
            with open(fp, 'wb') as f:
                f.write(buf[last_index: m.start()])
            last_index = m.start()

    def _decode_unknown_dat(self, dat_file):
        raise Exception('Unknown file type')


if __name__ == '__main__':
    import sys
    if len(sys.argv) != 2:
        print('\n'.join([
            'Usage:',
            '  python WechatImageDecoder.py [dat_file]',
            '',
            'Example:',
            '  # PC:',
            '  python WechatImageDecoder.py 1234567890.dat',
            '',
            '  # Android:',
            '  python WechatImageDecoder.py cache.data.10'
        ]))
        sys.exit(1)

    _,  path = sys.argv[:2]
    output = "./output"
    if len(sys.argv) == 3:
        output = sys.argv[2]
    try:
        if not os.path.isdir(path):
            WechatImageDecoder(path)
        else:
            for p,d,filelist in os.walk(path):
                #print d
                for filename in filelist:
                    file_path = os.path.join(p, filename)
                    print file_path
                    WechatImageDecoder(file_path,output)
        
    except Exception as e:
        print(e)
        sys.exit(1)
    sys.exit(0)
