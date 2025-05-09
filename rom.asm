org 0xF0000
bits 16

start:
    jmp $

times 0xFFF0 - ($ - $$) db 0

reset:
    jmp 0xF000:0x0000

times 0xFFFF - ($ - $$) + 1 db 0
