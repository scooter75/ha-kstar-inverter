"""Constants for the Kstar Inverter Modbus integration."""

DOMAIN = "kstar_inverter"

CONF_CONNECTION_TYPE = "connection_type"
CONF_SERIAL_PORT = "serial_port"
CONF_BAUDRATE = "baudrate"
CONF_HOST = "host"
CONF_PORT = "port"
CONF_SLAVE_ID = "slave_id"
CONF_SCAN_INTERVAL = "scan_interval"

CONN_TYPE_SERIAL = "serial"
CONN_TYPE_TCP = "tcp"

DEFAULT_NAME = "Kstar Inverter"
DEFAULT_CONNECTION_TYPE = CONN_TYPE_SERIAL
DEFAULT_SERIAL_PORT = "/dev/ttyUSB0"
DEFAULT_BAUDRATE = 9600
DEFAULT_HOST = "192.168.1.100"
DEFAULT_TCP_PORT = 502
DEFAULT_SLAVE_ID = 1
DEFAULT_SCAN_INTERVAL = 10

BAUDRATES = [2400, 4800, 9600]

# Operating Mode Mapping (Register 3030 Upper Byte)
OPERATING_MODES = {
    0x00: "System Initialization",
    0x01: "Waiting",
    0x02: "Pre-detection",
    0x03: "Normal",
    0x04: "Error",
    0x05: "Permanent Error",
    0x06: "Aging",
    0x07: "INV_DSP Burning",
    0x08: "ARM Burning",
    0x09: "BST_DSP Burning",
}

# Inverter Models (Register 3030 Lower Byte - Table 3.1.5)
INVERTER_MODELS = {
    0x00: "KSG-1KSM3",
    0x01: "KSG1.5KSM3",
    0x02: "KSG2KSM3",
    0x03: "KSG3KSM3",
    0x04: "KSG3.2KDM3",
    0x05: "KSG4KDM3",
    0x06: "KSG5KDM3",
    0x07: "KSG10K / KSG6KDM3",
    0x08: "KSG12K",
    0x09: "KSG15K",
    0x0A: "KSG17K",
    0x0B: "KSG20K",
    0x0C: "KSG30K",
    0x0D: "KSG40K",
    0x0E: "KSG50K",
    0x0F: "KSG60K",
    0x14: "KSG25KHV",
    0x15: "KSG36KHV",
    0x16: "KSG50KHV",
    0x17: "KSG60KHV",
    0x1E: "KSG8KTL",
    0x1F: "KSG10KTL",
    0x20: "KSG12KTL",
    0x21: "KSG25KTL",
    0x22: "KSG30KTL",
    0x23: "KSG33KTL",
    0x24: "KSG36KTL",
    0x25: "KSG40KTL",
    0x26: "KSG50KHVC",
    0x27: "KSG60KHVC",
    0x28: "KSG50K",
    0x29: "KSG50KHV",
    0x2A: "KSG60K",
    0x2B: "KSG60KHV",
    0x2C: "KSG70KHV",
    0x32: "KSG50KTL",
    0x33: "KSG60KTL",
    0x34: "KSG70KTL",
    0x35: "KSG80KTL",
    0x36: "KSG60KHVC",
    0x37: "KSG70KHVC",
    0x38: "KSG80KHVC",
    0x39: "KSG100KHVC",
    0x3B: "KSG110SL",
    0x3C: "KSG100CL",
    0x3D: "KSG136UM",
    0x3E: "KSG110CL",
    0x41: "KSG100UH",
    0x42: "KSG136UH",
    0x43: "KSG175UH",
    0x44: "KSG200UH",
    0x45: "KSG225UH",
    0x64: "BluE-G 3000S",
    0x65: "BluE-G 3000D",
    0x66: "BluE-G 3600D",
    0x67: "BluE-G 4000D",
    0x68: "BluE-G 4200D",
    0x69: "BluE-G 4600D",
    0x6A: "BluE-G 5000D",
    0x6B: "BluE-G 6000D",
    0x6E: "BluE-3KT-M0",
    0x6F: "BluE-3KT-M1",
    0x70: "BluE-3.6KT-M0",
    0x71: "BluE-3.6KT-M1",
    0x72: "BluE-4KT-M0",
    0x73: "BluE-4KT-M1",
    0x74: "BluE-5KT-M0",
    0x75: "BluE-5KT-M1",
    0x76: "BluE-6KT-M0",
    0x77: "BluE-6KT-M1",
    0x78: "BluE-8KT-M0",
    0x79: "BluE-8KT-M1",
    0x7A: "BluE-10KT-M0",
    0x7B: "BluE-10KT-M1",
    0x7C: "BluE-12KT-M0",
    0x7D: "BluE-12KT-M1",
    0x7E: "BluE-15KT-M0",
    0x7F: "BluE-15KT-M1",
    0x80: "BluE-15KT-M2",
    0x81: "BluE-15KT-M3",
    0x82: "BluE-17KT-M0",
    0x83: "BluE-17KT-M1",
    0x84: "BluE-20KT-M0",
    0x85: "BluE-20KT-M1",
    0x86: "BluE-22KT-M0",
    0x87: "BluE-22KT-M1",
    0x88: "BluE-23KT-M0",
    0x89: "BluE-23KT-M1",
    0x8A: "BluE-25KT-M0",
    0x8B: "BluE-25KT-M1",
    0x8C: "KSG-25KT-M0",
    0x8D: "KSG-25KT-M1",
    0x8E: "KSG-25KT-M2",
    0x8F: "KSG-25KT-M3",
    0x90: "KSG-30KT-M0",
    0x91: "KSG-30KT-M1",
    0x92: "KSG-30KT-M2",
    0x93: "KSG-30KT-M3",
    0x94: "KSG-30KT-M4",
    0x95: "KSG-30KT-M5",
    0x96: "KSG-33KT-M0",
    0x97: "KSG-33KT-M1",
    0x98: "KSG-33KT-M2",
    0x99: "KSG-33KT-M3",
    0x9A: "KSG-33KT-M4",
    0x9B: "KSG-33KT-M5",
    0x9C: "KSG-36KT-M0",
    0x9D: "KSG-36KT-M1",
    0x9E: "KSG-36KT-M2",
    0x9F: "KSG-36KT-M3",
    0xA0: "KSG-36KT-M4",
    0xA1: "KSG-36KT-M5",
    0xA2: "KSG-40KT-M0",
    0xA3: "KSG-40KT-M1",
    0xA4: "KSG-40KT-M2",
    0xA5: "KSG-40KT-M3",
    0xA6: "KSG-40KT-M4",
    0xA7: "KSG-40KT-M5",
    0xA8: "G80KT",
    0xA9: "G80KT1",
    0xAA: "G75KT",
    0xAB: "G75KT1",
    0xAC: "G70KT",
    0xAD: "G70KT1",
    0xAE: "G60KT",
    0xAF: "G60KT1",
    0xB0: "G50KT",
    0xB1: "G50KT1",
    0xB2: "G40KT",
    0xB3: "G40KT1",
    0xB4: "G40KT2",
    0xB5: "G40KT3",
}

# DSP Alarm Bits (Register 3027 - Table 3.1.2)
DSP_ALARM_CODES = {
    0: "W00: Fan A Lock",
    1: "W01: Fan B Lock",
    2: "W02: Fan C Lock",
    3: "W03: Zero Power",
    4: "W04: Array Warning",
    6: "W06: Lightning Warning",
    7: "W07: PV Parallel Open",
}

# DSP Error Bits (Registers 3028-3029 - Table 3.1.3)
DSP_ERROR_CODES = {
    0: "F00: Grid Volt Low",
    1: "F01: Grid Volt High",
    2: "F02: Grid Frequency Low",
    3: "F03: Grid Frequency High",
    4: "F04: Bus Volt Low",
    5: "F05: Bus Volt High",
    6: "F06: Bus Volt Unbalance",
    7: "F07: Isolation Fault",
    8: "F08: PV Current High",
    9: "F09: Hard Inverter Current Over",
    10: "F10: Inverter Current Over",
    11: "F11: Inverter DC Current Over",
    12: "F12: Ambient Temperature Over",
    13: "F13: Sink Temperature Over",
    14: "F14: AC Relay Fault",
    16: "F16: Remote Off",
    18: "F18: SPI Communication Fail",
    19: "F19: SPI2 Communication Fail",
    20: "F20: GFCI Over Fault",
    21: "F21: GFCI Device Fault",
    22: "F22: Voltage Consistent Fault",
    23: "F23: Frequency Consistent Fault",
    25: "F25: Auxiliary Power Off",
    26: "F26: IGBT Fault",
    27: "F27: NPE Volt Fault",
    28: "F28: DC Over Volt Serious Fault",
    29: "F29: IGBT Serious Fault",
}

# Control / Write Registers (Function Code 0x06 - Table 3.4.1)
REG_CLEAR_STATS = 4000
REG_REMOTE_OFF = 4001
REG_REVOKE_REMOTE_OFF = 4002
REG_SET_POWER_FACTOR = 4003
REG_SET_ACTIVE_POWER_PCT = 4004
REG_SET_REACTIVE_POWER_KVAR = 4005
REG_SET_REACTIVE_MODE = 4006
REG_SET_ACTIVE_POWER_KW = 4010
REG_SET_BACK_CURRENT_LIMIT = 4020
REG_REMOTE_CONTROL_ENABLE = 4029
REG_CLEAR_FAULT_RECORD = 4033
REG_START_IV_SCAN = 4035
