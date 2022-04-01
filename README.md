## CG2028 ASM to machine code converter
The python script converts asm instructions to 32 bit machine code as per CG2028 requirements.

<img width="1352" alt="image" src="https://user-images.githubusercontent.com/55841532/161284264-5889f0fa-ea26-4bd8-b8be-8faefea6d57e.png">

# Notes
- Needs Python 3.8 and above to run code.
- PC relative indexing not supported.
- No exception handling at the moment.
- Normal LDR instruction without offset may have discrepencies. Always please self-check output to be sure.
