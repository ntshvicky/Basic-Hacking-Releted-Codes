from PIL import Image
import binascii
import optparse

def encode(hex_data, digit):
    if hex_data[-1] in ('0', '1', '2', '3', '4', '5'):
        hex_data = hex_data[:-1] + digit
        return hex_data
    else:
        return None

def hide(filename, message):
    img = Image.open(filename)
    binary_msg = bin(int(binascii.hexlify(message.encode()), 16))[2:]
    if img.mode in ('RGB'):
        img = img.convert('RGB')
        datas = img.getdata()
        
        new_data = []
        digit = 0
        temp = ''
        for item in datas:
            if digit < len(binary_msg):
                newpix = encode('{0:02x}{1:02x}{2:02x}'.format(item[0], item[1], item[2]), binary_msg[digit])
                if newpix == None:
                    new_data.append(item)
                else:
                    r, g, b = int(newpix[0:2], 16), int(newpix[2:4], 16), int(newpix[4:6], 16)
                    new_data.append((r, g , b))
                    digit += 1
            else:
                new_data.append(item)
        img.putdata(new_data)
        img.save(filename, "PNG")
        return "Completed!"
    return "Incorrect Image Mode, Couldn't Hide"

def decode(filename):
    img = Image.open(filename)
    binary_data = ""
    
    if img.mode in ('RGB'):
        img = img.convert('RGB')
        datas = img.getdata()
        
        for item in datas:
            digit = decode_pixel(item[0]) + decode_pixel(item[1]) + decode_pixel(item[2])
            binary_data += digit
            if (binary_data[-16:] == '1111111111111110'):
                break

    # Convert binary data to hex
    hex_data = ''
    for i in range(0, len(binary_data), 8):
        byte = binary_data[i:i+8]
        hex_data += '%02x' % int(byte, 2)

    print("Extracted Hex Data:", hex_data)  # Print out the extracted hex data

    try:
        return binascii.unhexlify(hex_data).decode('utf-8')
    except UnicodeDecodeError as e:
        print("Unicode Decode Error:", e)
        return None

def decode_pixel(val):
    if val % 2 == 0:
        return '0'
    else:
        return '1'

# Rest of the code remains the same



def main():
    parser = optparse.OptionParser('usage %prog ' + '-e/-d <target file>')
    parser.add_option('-e', dest='hide', type='string', help='target picture path to hide text')
    parser.add_option('-t', dest='text', type='string', help='text to hide in picture')
    
    (options, args) = parser.parse_args()
    if options.hide != None and options.text != None:
        print(hide(options.hide, options.text))
    else:
        print(parser.usage)
        exit(0)

    secret = decode('1.jpg')
    print("Hidden message:", secret)

if __name__ == '__main__':
    main()


# python steganography.py -e 1.jpg -t "My name is anthony gonzalez"
