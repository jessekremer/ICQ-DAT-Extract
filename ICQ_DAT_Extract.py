import sys
import struct
from datetime import datetime

SKIP_HEADER_BYTES=672
MSG_HEADER =        b'\x61\x72\x69\x4D\x20\x67\x73\x4D\x03'
MSG_HEADER_ALT =    b'\x61\x72\x69\x4D\x67\x73\x4D\x50\x03'

output_filename = 'formatted_log.txt'

me = b'@h\x95\x05IE3\x04\x01\x00'
me_again = b'\xe6N\x11\x03@h\x95\x05\x01\x00'
# msg start 6172694D2067734D03000000
# skip 2 bytes
# 10 bytes = user
# next 7 bytes = unsure
# next byte = reply type?
# 1 byte = blank
# message text

def read_binary_file(filename):
    try:
        with open(filename, "rb") as f:
            f.seek(SKIP_HEADER_BYTES)  # Skip first 672 bytes. Unknown header.
            data = f.read()  # Read the rest of the file
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    with open(output_filename, "w") as file:
        index = 0 # Start searching from the beginning of the remaining data
        index_alt = index
        while index < len(data):
            og_index = index
            index = data.find(MSG_HEADER, index)  # Find next match
            header_version = MSG_HEADER
            index_alt = data.find(MSG_HEADER_ALT, og_index)  # Find next match
            if index_alt < index :
                index = index_alt
                header_version = MSG_HEADER_ALT

            # get the unix formatted datetime
            chunk = data[index+12:index+16]
            int_value = struct.unpack("<I", chunk)[0]

            if 0 < int_value < 2**31:  # Only consider valid positive timestamps
                date_value = datetime.utcfromtimestamp(int_value).strftime('%Y-%m-%d %H:%M:%S UTC')
            else:
                date_value = "Not a valid timestamp"
            
            icq_num = data[index+16:index+20] #icq number

            if index == -1:
                break  # Stop if no more matches
            
            user = struct.unpack("<I", icq_num)[0] # convert the icq_num into an actual number
            reply_type = data[index+32:index+33].hex() # unsure what this is for

            # the message body is from the header end, to the first 00 hex value
            message = data[index+34:data.find(b'\x00', index+34)]
            message = message.decode('utf-8',errors="ignore")
            
            # write to text file
            file.write(f"{user}"+" ["+date_value+"]: "+message+"\n")

            index += len(header_version)  # Move past this match to find the next

        if index == 0:
            print("Pattern not found in the file.")
            
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <filename>")
    else:
        read_binary_file(sys.argv[1])