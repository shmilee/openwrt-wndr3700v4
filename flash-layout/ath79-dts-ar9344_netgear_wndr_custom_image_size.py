#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2025 shmilee

'''
create 'ar9344_netgear_wndr_custom_image_size.dtsi'.
'''

import os
import sys
import argparse

NODES_TODO = '''
		partition@6c0000 {
			label = "firmware";
			reg = <0x6c0000 0x1900000>;

			compatible = "fixed-partitions";
			#address-cells = <1>;
			#size-cells = <1>;

			kernel@0 {
				label = "kernel";
				reg = <0x0 0x400000>;
			};

			ubiconcat0: partition@400000 {
				label = "ubiconcat0";
				reg = <0x400000 0x1500000>;
			};
		};

		partition@1fc0000 {
			label = "caldata_backup";
			reg = <0x1fc0000 0x40000>;
			read-only;
		};

		ubiconcat1: partition@2000000 {
			label = "ubiconcat1";
			reg = <0x2000000 0x6000000>;
		};
	};
'''


def get_new_nodes(image_size):
    '''image_size: str, endswith m or k'''
    if image_size[-1] not in ('m', 'k'):
        raise ValueError("image_size should ends with m or k!")
    if image_size[-1] == 'm':
        image_size = int(image_size[:-1])*1024*1024
    elif image_size[-1] == 'k':
        image_size = int(image_size[:-1])*1024
    __121M = 121 * 1024 * 1024
    if not (0 < image_size < __121M):
        raise ValueError("image_size should be between 0 and 121M!")
    # 1. firmware
    firmware_len = '0x%x' % image_size
    tmp = NODES_TODO.replace('0x1900000', firmware_len)
    ubiconcat0_len = '0x%x' % (image_size - 0x400000)
    tmp = tmp.replace('0x1500000', ubiconcat0_len)
    # 2. caldata_backup
    caldata_backup_start = '%x' % (0x6c0000 + image_size)
    tmp = tmp.replace('1fc0000', caldata_backup_start)
    # 3. ubiconcat1
    ubiconcat1_start = '%x' % (0x6c0000 + image_size + 0x40000)
    ubiconcat1_len = '0x%x' % (__121M - image_size)
    tmp = tmp.replace('2000000', ubiconcat1_start)
    tmp = tmp.replace('0x6000000', ubiconcat1_len)
    return tmp


def replace_dtsi(original, custom, image_size='25m'):
    '''
    original, custom: path
    image_size: str, like '25m', '25600k', '36m', '37748736k', etc.
    '''
    with open(original, 'r') as orig:
        old_dtsi = orig.read()
        if NODES_TODO not in old_dtsi:
            raise ValueError("Invalid netgear_wndr dtsi file!")
        NODES_DONE = get_new_nodes(image_size)
        new_dtsi = old_dtsi.replace(NODES_TODO, NODES_DONE)
        with open(custom, 'w') as out:
            out.write(new_dtsi)


def main():
    parser = argparse.ArgumentParser(
        description='custom netgear_wndr image_size',
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument(
        '--imgsize', dest='imgsize', nargs='?', type=str, default='25m',
        help="image_size, like '25m', '25600k' (default: %(default)s)")
    parser.add_argument(
        'original_dtsi', metavar='path/to/dtsi', nargs='?', type=str,
        help='the path of original ar9344_netgear_wndr.dtsi\n'
             'For example, target/linux/ath79/dts/ar9344_netgear_wndr.dtsi')
    args = parser.parse_args()

    if not args.original_dtsi:
        parser.print_help()
        sys.exit(1)
    if not os.path.isfile(args.original_dtsi):
        print("[E] %s not found!" % args.original_dtsi)
        sys.exit(2)
    prefix, ext = os.path.splitext(args.original_dtsi)
    custom_dtsi = prefix + '_custom_image_size.dtsi'
    replace_dtsi(args.original_dtsi, custom_dtsi, args.imgsize)
    print("[I] Please check the custom dtsi in '%s'." % custom_dtsi)
    sys.exit(0)

if __name__ == '__main__':
    main()
