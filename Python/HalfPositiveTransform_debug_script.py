import struct
import nuke

"""
This script is meant to be used inside of Nuke, to help debug the HaflPositiveTransform nodes by displaying pixel values at each steps. 
"""

def float_to_ieee754_32(value: float) -> str:
    # Conversion float 32 bits IEEE 754
    packed = struct.pack('>f', value)  # '>f' = big-endian float (32 bits)
    binary_str = ''.join(f'{byte:08b}' for byte in packed)
    sign = binary_str[0]
    exponent = binary_str[1:9]
    mantissa = binary_str[9:]
    formatted_mantissa = ' '.join([mantissa[i:i+4] for i in range(0, len(mantissa), 4)])
    hex_str = packed.hex()
    return f"{sign} {exponent} {formatted_mantissa}", hex_str


def float_to_ieee754_16(value: float) -> str:
    # Conversion float 16 bits IEEE 754 (half precision)
    packed = struct.pack('>e', value)  # '>e' = big-endian half-precision float (16 bits)
    binary_str = ''.join(f'{byte:08b}' for byte in packed)
    sign = binary_str[0]
    exponent = binary_str[1:6]
    mantissa = binary_str[6:]
    formatted_mantissa = ' '.join([mantissa[i:i+4] for i in range(0, len(mantissa), 4)])
    hex_str = packed.hex()
    return f"{sign} {exponent} {formatted_mantissa}", hex_str


def convert_float_to_ieee754(value: float):
    #print(f"Converting the float value: {value}\n")

    # 32-bit conversion
    binary_32, hex_32 = float_to_ieee754_32(value)
    print("32-bit IEEE 754 representation:")
    print(f"Binary:  {binary_32}")
    print(f"Hex:     0x{hex_32}\n")

    # 16-bit conversion
    binary_16, hex_16 = float_to_ieee754_16(value)
    print("16-bit IEEE 754 representation:")
    print(f"Binary:  {binary_16}")
    print(f"Hex:     0x{hex_16}\n")

coordX = 1721
coordY = 1114
Chan = 'g'
base_input = nuke.sample(nuke.toNode('ColorWheel1'), Chan, coordX, coordY)
blink_convert = nuke.sample(nuke.toNode('BlinkScript1'), Chan, coordX, coordY)
transfered_infos = nuke.sample(nuke.toNode('BlinkScript1'), 'a', coordX, coordY)
blink_out = nuke.sample(nuke.toNode('BlinkScript2'), Chan, coordX, coordY)

print("\n"+"="*10 + ' Base value: ')
convert_float_to_ieee754(base_input)
print("="*10 + ' Blink conversion: ')
convert_float_to_ieee754(blink_convert)
print("="*10 + ' Infos channels: ')
convert_float_to_ieee754(transfered_infos)
print("="*10 + ' Out value: ')
convert_float_to_ieee754(blink_out)