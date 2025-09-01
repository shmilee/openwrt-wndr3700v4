#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2025 shmilee

'''
create 'ar9344_netgear_wndr3700-v4-custom-XXm.dts'
'''

import os
import sys
import argparse

RAW_DTS_CONTENT = '''// SPDX-License-Identifier: GPL-2.0-or-later OR MIT

#include "ar9344_netgear_wndr.dtsi"
#include "ar9344_netgear_wndr_wan.dtsi"
#include "ar9344_netgear_wndr_usb.dtsi"

/ {
	compatible = "netgear,wndr3700-v4", "qca,ar9344";
	model = "Netgear WNDR3700 v4";
};
'''


def update_nand_nodes(image_size):
    '''
    image_size: str, endswith m or k,
        like '25m', '25600k', '36m', '37748736k', etc.
    '''
    if image_size[-1] not in ('m', 'k'):
        raise ValueError("image_size should ends with m or k!")
    if image_size[-1] == 'm':
        image_size = int(image_size[:-1])*1024*1024
    elif image_size[-1] == 'k':
        image_size = int(image_size[:-1])*1024
    if not (0x400000 < image_size < 0x7900000):
        raise ValueError("image_size should be between 4M and 121M!")
    # 1. firmware
    firmware_len = image_size
    ubiconcat0_len = image_size - 0x400000
    # 2. caldata_backup
    caldata_backup_start = 0x6c0000 + image_size
    # 3. ubiconcat1
    ubiconcat1_start = 0x6c0000 + image_size + 0x40000
    ubiconcat1_len = 0x7900000 - image_size
    return f'''
&nand {{
	partitions {{

		partition@6c0000 {{
			reg = <0x6c0000 0x{firmware_len:x}>;

			ubiconcat0: partition@400000 {{
				reg = <0x400000 0x{ubiconcat0_len:x}>;
			}};
		}};

		/delete-node/ partition@1fc0000;
		/delete-node/ ubiconcat1;

		partition@{caldata_backup_start:x} {{
			label = "caldata_backup";
			reg = <0x{caldata_backup_start:x} 0x40000>;
			read-only;
		}};

		ubiconcat1: partition@{ubiconcat1_start:x} {{
			label = "ubiconcat1";
			reg = <0x{ubiconcat1_start:x} 0x{ubiconcat1_len:x}>;
		}};

	}};
}};
'''


def create_dts(original, custom, image_size='25m'):
    '''
    original, custom: path
    '''
    if not os.path.isfile(original):
        raise OSError(f"{original} not found!")
    with open(original, 'r') as orig:
        old_dts = orig.read()
        if RAW_DTS_CONTENT.strip() != old_dts.strip():
            raise ValueError("Invalid ar9344_netgear_wndr3700-v4.dts!")
        NODES_DONE = update_nand_nodes(image_size)
        with open(custom, 'w') as out:
            out.write(RAW_DTS_CONTENT)
            out.write(NODES_DONE)


def main():
    parser = argparse.ArgumentParser(
        description='custom netgear_wndr3700-v4 image_size',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--imgsize', dest='imgsize', nargs='?', type=str, default='25m',
        help="image_size, like '25m', '25600k' (default: %(default)s)")
    parser.add_argument(
        'original_dts', metavar='path/to/dts', nargs='?', type=str,
        help='the path of original ar9344_netgear_wndr3700-v4.dts\n'
             'For example, target/linux/ath79/dts/ar9344_netgear_wndr3700-v4.dts')
    args = parser.parse_args()

    if not args.original_dts:
        parser.print_help()
        sys.exit(1)

    prefix, ext = os.path.splitext(args.original_dts)
    custom_dts = prefix + f'-custom-{args.imgsize}.dts'
    create_dts(args.original_dts, custom_dts, args.imgsize)
    print("[I] Please check the custom dts in '%s'." % custom_dts)
    sys.exit(0)


if __name__ == '__main__':
    main()
