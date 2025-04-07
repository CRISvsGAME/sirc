#!/usr/bin/env bash

dd if=/dev/zero of=rom.bin bs=1 count=$((64 * 1024))

printf "\xEB\xFE" | dd of=rom.bin bs=1 seek=$((0xFFF0)) conv=notrunc
