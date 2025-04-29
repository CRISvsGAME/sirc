#!/usr/bin/env bash

dd if=/dev/zero of=rom.bin bs=1 count=$((64 * 1024))

printf "\xEA\x00\x00\x00\xF0" | dd of=rom.bin bs=1 seek=$((0xFFF0)) conv=notrunc

printf "\xEB\xFE" | dd of=rom.bin bs=1 seek=$((0x0000)) conv=notrunc
