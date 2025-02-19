# ICQ-DAT-Extract
I found my old ICQ DAT and IDX files from 2000/2001 on a hard drive, that I want to reconstruct and read.
I was using a PPC Mac at the time on OS 9, so perhaps there are some differences to the existing tools and this is helpful to someone.

## Usage
Locate your DAT file (for example mine is 93677632.msg.dat) and run:  
```python ICQ_DAT_Extract.py 93677632.msg.dat```

A file titled formatted_log.txt will be generated in this location.

## Limitations
Currently, this version only extracts the messages in the binary DAT file in chronological order. I haven't worked out how the IDX file works for linking conversations together. My intention is to incorporate the IDX file too and generate a simple HTML page output to browse the conversations.  
If you are having issues and are willing to share your DAT file, let me know as I may be able to tweak it to also use your file.