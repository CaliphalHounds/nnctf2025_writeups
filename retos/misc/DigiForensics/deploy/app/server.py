from hashlib import md5

item_table = [
    "hp restore small",
    "hp restore mid",
    "hp restore large",
    "sp restore small",
    "sp restore mid",
    "sp restore large",
    "mp restore small",
    "mp restore mid",
    "mp restore large",
    "special mission 1",
    "special mission 2",
    "special mission 3",
    "special mission 4",
    "atk+",
    "atk+ large",
    "def+",
    "def+ large",
    "abi+",
    "abi+ large",
    "cube",
    "strange candy",
    "MT13"
    "evolution ticket",
    "digivice",
    "hard drive",
    "memory card",
    "RAM upgrade",
    "CPU upgrade",
    "large meat",
    "game boy advance",
    "win-rar install disc",
    "FLAG",
]
   

if __name__ == "__main__":
    print("<READY>")
    rom = input("DATA OK> ")
    
    rom = [ packet.upper() for packet in rom.split("-") ]
        
    if all([len(packet) == 32 for packet in rom]) and len(rom) == 4:
        print("ROM OK")
        
    else: 
        print("ROM ERROR")
        exit(1)
    
    signature1 = rom[0][0:8]
    signature2 = rom[1][0:8]
    order = rom[0][8]
    version = rom[0][11]
    operation = rom[0][12:14]
    flow_control1 = rom[0][14:16]
    flow_control2 = rom[1][8:10]
    
    packet1_data = rom[0][0:16]
    packet2_data = rom[1][0:16]
    
    checksum1 = rom[0][16:32]
    checksum2 = rom[1][16:32]
    slot = rom[1][10:12]
    item_id = rom[1][12:16]
    
    correct_checksums = all([packet[16:32].upper() == md5(bytes.fromhex(packet[0:16])).hexdigest().upper()[:16] for packet in rom])
    
    if correct_checksums:
        print("MD5 CHECKSUM OK")
        
    else:
        print("MD5 CHECKSUM ERROR")
        exit(1)
    
    if signature1 == "4E414341" and signature2 == "4E414341":
        print("SIGNATURE OK")
        
    else:
        print("SIGNATURE ERROR")
        exit(1)
        
    if flow_control1 != "00" and flow_control2 != "01":
        print("FLOW CONTROL ERR")
        exit(1)

    else:
        print("FLOW CONTROL OK")
    

    if order != "1":
        print("CANNOT INITIATE")
        exit(1)
        
    if operation != "08":
        print(f"INVALID OPERATION {operation.upper()}")
        exit(-1)
        
    item_id = int(item_id, 16)
    if version != "D":
        object_name = item_table[item_id % (len(item_table) - 1)]
        packet2_resp = f"4E4143410100{hex(item_id % (len(item_table) - 1))[2:].upper().zfill(4)}"
        
    else:
        object_name = item_table[item_id  % (len(item_table))]
        packet2_resp = f"4E4143410100{hex(item_id % (len(item_table)))[2:].upper().zfill(4)}"
    
    packet2_checksum = md5(bytes.fromhex(packet2_resp)).hexdigest().upper()[:16]
    
    print(f"SENT {object_name.upper()} INTO SLOT {int(slot, 16)}")
    
    
    if object_name == "FLAG":
        print(f"4E41434111440000B09AA1A02BC1A125-{packet2_resp}{packet2_checksum}-6E6E6374667B5033071CB1BF90B8C573-743467306368317DC4CE01600E18ED94")
        exit(1)
        
    else:
        print(f"4E41434111440000B09AA1A02BC1A125-{packet2_resp}{packet2_checksum}-00000000000000007DEA362B3FAC8E00-00000000000000007DEA362B3FAC8E00")
        exit(0)
