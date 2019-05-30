import sys
import math
BYTEORDER = 'big'
OUTPUT_FILE = './output_lzss_encoder.bin'
class node:
    def __init__(self, value, frequnecy, left=None, right=None):
        self.value = value
        self.freq = frequnecy
        self.left = left
        self.right = right
        return


class huffman:
    def __init__(self, s):
        if type(s) is str:
            self.construct_tree(s)
        elif type(s) is dict:
            self.code_dict = s
        else:
            assert False
    def construct_tree(self, s):
        freq_list = get_freq(s)
        for i in range(len(freq_list)):
            freq_list[i] = node(freq_list[i][0], freq_list[i][1])
        while len(freq_list) != 1:
            new_node = huffman.merge(freq_list[0], freq_list[1])
            freq_list = freq_list[2:]
            for i in range(len(freq_list)):
                if new_node.freq <= freq_list[i].freq:
                    freq_list = [*freq_list[:i], new_node, *freq_list[i:]]
                    break
            else:
                freq_list.append(new_node)
        self.root = freq_list[0]
        self.code_dict = self.extract_encoding()
        self.s = s
    def encode(self, plaintext=None):
        if plaintext is None:
            plaintext = self.s
        codeword = ''
        for i in plaintext:
            codeword += self.code_dict[i]
        return codeword

    @staticmethod
    def merge(a, b):
        if a.freq > b.freq:
            a, b = b, a
        new_node = node(a.value+b.value, a.freq+b.freq, a, b)
        return new_node

    def extract_encoding(self):
        encoding_dict = self.traverse(self.root, '')
        return encoding_dict

    def traverse(self, current, encoding):
        if current.left is None and current.right is None:
            return {current.value: encoding}
        left_sub = self.traverse(current.left, encoding + '0')
        right_sub = self.traverse(current.right, encoding+'1')
        left_sub.update(right_sub)
        return left_sub
    def decode(self, codeword, code_dict=None):
        if code_dict is None:
            if self.code_dict is None:
                raise Exception('huffman encoding mapping must be provided')
            code_dict = self.code_dict
        if codeword == '':
            return ''
        assert type(codeword) is str
        decoder_dict = dict(map(reversed, code_dict.items()))
        plaintext = ''
        end = 0
        while end <= len(codeword)-1:
            if codeword[:end + 1] in decoder_dict.keys():
                plaintext = decoder_dict[codeword[:end+1]]
                break
            else:
                end += 1
        if plaintext == '':
            raise Exception('dict not correct')
        return plaintext, codeword[end+1:]
    def decode_all(self, codeword, code_dict=None):
        plaintext = ''
        rest = codeword 
        while rest != '':
            current_plaintext, rest = self.decode(rest, code_dict)
            plaintext += current_plaintext
        return plaintext



def get_freq(charlist):
    freq_dict = {}
    for c in charlist:
        freq_dict[c] = freq_dict.get(c, 0) + 1
    freq_list = sorted(freq_dict.items(), key=lambda x: x[1])
    return freq_list

class elias:
    def __init__(self):
        pass
    
    def encode(self, N):
        N += 1
        if N < 1:
            raise Exception('cannot encode negatives')
        if int(N) != N:
            raise Exception('cannot encode non-integer')
        if N == 1:
            return '1'
        
        return self.get_lcomp(N)+self.to_bin(N)

    def get_lcomp(self, L):
        lbin = self.to_bin(L)
        lcomp = len(lbin) - 1
        if lcomp == 1:
            return '0'
        return self.get_lcomp(lcomp) + '0' + self.to_bin(lcomp)[1:]
    def to_bin(self, N):
        return bin(N)[2:]
    def decode(self, codeword):
        assert type(codeword) is str
        if codeword[0] == '1':
            return 0, codeword[1:]
        readlen = 1
        l_comp = ''
        pos = 0
        while codeword[pos] != '1':
            l_comp = codeword[pos:pos+readlen]
            assert l_comp != ''
            pos = pos + readlen
            readlen = int('1' + l_comp[1:], 2)+1

        plaintext = int(codeword[pos:pos+readlen], 2) - 1
        return plaintext, codeword[pos+readlen:]

    # this function is just for testing, will not be used in main routine
    def decode_all(self, codeword):
        plaintext = []
        rest = codeword 
        while rest != '':
            current_plaintext, rest = self.decode(rest)
            plaintext.append(current_plaintext)
        return plaintext


def read_cmdarg():
    if len(sys.argv) != 4:
        raise Exception("input not in correct format")
    return sys.argv[1], sys.argv[2], sys.argv[3]

def readfile_txt(filepath):
    with open(filepath, 'r',  encoding='utf-8-sig') as fobject:
        content = fobject.read()
    return content

def test_elias(max_text_num=100, test_num=10):
    from random import choices
    test_nums = choices(range(max_text_num), k=test_num)
    codeword = ''
    for i in test_nums:
        codeword += elias().encode(i)
    plaintext = elias().decode_all(codeword)
    assert test_nums == plaintext

def test_huffman(stringLength=10000):

    from random import choices
    import string
    letters = string.printable

    rand_str = ''.join(choices(letters, k=stringLength))
    encoder = huffman(rand_str)
    codeword = encoder.encode()
    decoder = huffman(encoder.code_dict)
    plaintext = decoder.decode_all(codeword)
    assert rand_str == plaintext

class LZSS:
    def __init__(self, window_size=None, buffer_size=None, fobject=None):
        self.window_size = window_size
        self.buffer_size = buffer_size
        self.huffman_encoder = None
        self.fobject = fobject
        self.elias_encoder = elias()
    def tuple_encode(self, t):
        if t[0] == 1:
            tuple_code = '1'+self.huffman_encoder.encode(t[1])
            return tuple_code
        elif t[0] == 0:
            tuple_code = '0'+self.elias_encoder.encode(t[1])+self.elias_encoder.encode(t[2])
            return tuple_code
        else:
            assert False
    def encode(self, data, window_size=None, buffer_size=None):
        if len(data)== 0:
            return ''
        self.huffman_encoder = huffman(data)
        window_size = self.window_size or window_size
        buffer_size = self.buffer_size or buffer_size
        assert window_size is not None and buffer_size is not None
        field_num = 1
        codeword = self.tuple_encode((1, data[0]))
        buffer_start = 1
        while buffer_start <= len(data) - 1:  
            i = max(buffer_start - window_size, 0)
            max_match_start = None
            max_match_length = 0
            while i < buffer_start:
                j = buffer_start
                k = i 
                while j <= len(data)-1:
                    if data[k] != data[j]:
                        break
                    else:
                        k+=1
                        j+=1
                if k - i > max_match_length:
                    max_match_length = k - i
                    max_match_start = i 
                
                i += 1
            if max_match_length < 3:
                codeword += self.tuple_encode((1, data[buffer_start]))
                buffer_start += 1
            else:
                offset = buffer_start - max_match_start
                
                codeword += self.tuple_encode((0, offset, max_match_length))
                buffer_start += max_match_length
            field_num += 1
        codeword = elias().encode(field_num) + codeword
        return codeword

    @staticmethod
    def decode(codeword, huffman_encode_dict, field_num):
        elias_decoder = elias()
        huffman_decoder = huffman(huffman_encode_dict)
        tuple_list = []
        rest = codeword
        while field_num != 0:
            fst_bit = int(rest[0])
            rest = rest[1:]
            if fst_bit == 1:
                plainchar, rest = huffman_decoder.decode(rest)
                tuple_list.append((fst_bit, plainchar))
            elif fst_bit == 0:
                offset, rest = elias_decoder.decode(rest)
                length, rest = elias_decoder.decode(rest)
                tuple_list.append((fst_bit, offset, length))
            else:
                raise Exception("decoding error")
            field_num-=1
        assert tuple_list[0][0] == 1
        plaintext = ''
        while len(tuple_list) != 0:
            current_t = tuple_list[0]
            tuple_list= tuple_list[1:]
            if current_t[0] == 1:
                plaintext += current_t[1]
            else:
                match_start = len(plaintext) - current_t[1]
                match_length = current_t[2]
                while match_length != 0:
                    plaintext += plaintext[match_start]
                    match_start+=1
                    match_length-=1
                
        return plaintext

def generate_header(data):
    # encode number of unique ASCII char in elias
    # for each unique char 
        # encode using 8bit ascii
        # encode using elias the length of huffman code assigned to char
        # concatenate the huffman codeword assigned to that unique char
    elias_encoder = elias()
    huffman_encoder = huffman(data)
    header = ''
    header += elias_encoder.encode(len(huffman_encoder.code_dict))
    for plainchar, encoding in huffman_encoder.code_dict.items():
        char_in_ascii = bin(ord(plainchar))[2:]
        char_in_ascii = (8-len(char_in_ascii))*'0'+char_in_ascii
        header += char_in_ascii + elias_encoder.encode(len(encoding)) + encoding
    return header
def decode_header(codeword):
    elias_decoder = elias()
    char_nums, rest = elias_decoder.decode(codeword)
    huffman_dict = {}
    for i in range(char_nums):
        char_ascii = chr(int(rest[:8], 2))
        rest = rest[8:]
        huffman_code_len, rest = elias_decoder.decode(rest)
        huff_encoding = rest[:huffman_code_len]
        rest = rest[huffman_code_len:]
        huffman_dict[char_ascii] = huff_encoding
    return huffman_dict, rest

def decode_info(codeword, huffman_encode_dict):
    elias_decoder = elias()
    tuple_num, rest = elias_decoder.decode(codeword)
    plaintext = LZSS.decode(rest, huffman_encode_dict, tuple_num)
    return plaintext
        
def decode(codeword):
    huffman_encode_dict, codeword_info = decode_header(codeword)
    plaintext = decode_info(codeword_info, huffman_encode_dict)
    return plaintext

def test_LZSS(stringLength=1000, window_size_range=range(1,10),buffer_size_range=range(1,10), test_num=10):
    test_elias()
    test_huffman()
    from random import choices
    import string
    letters = string.ascii_letters

    for i in range(test_num):
        rand_str = ''.join(choices(letters, k=stringLength))
        for window_size in window_size_range:
            for buffer_size in buffer_size_range:
                codeword = encode(rand_str,window_size,buffer_size)
                plaintext = decode(codeword)

        assert plaintext == rand_str


def encode(data, window_size, buffer_size, write_to_file_path=OUTPUT_FILE):
    with open(OUTPUT_FILE, 'ab') as fobject:
        header = generate_header(data)
        # print(header)
        # print(int(header))
        # fobject.writelines(bytearray(int(header, 2)))

        LZSS_encoder = LZSS(window_size=window_size,
                            buffer_size=buffer_size, fobject=fobject)
        information = LZSS_encoder.encode(data)
        # for i in range(len())
        # print(header+information)
        return header + information



# def test_all():
#     from random import choices
#     import string
#     letters = string.printable
#     stringLength=2120
#     test_num=1
#     for i in range(test_num):
#         rand_str = ''.join(choices(letters, k=stringLength))
#         # print(str(len(rand_str)) + ' uncompressed size')
#         codeword_bin = encode(rand_str, 6,4)
#         writefile_bin(codeword_bin)
#         read_bin = readfile_bin()
#         assert decode(read_bin) == rand_str


def binstr_to_bytearray(data):
    int_array = []
    for i in range(0, len(data), 8):
        next_byte = data[i:i+8]
        next_byte = int(next_byte, 2)

        int_array.append(next_byte)
    return bytearray(int_array)


def bytearray_to_binstr(data):
    result_binstr = ''.join(
        list(map(lambda x: (8-len(bin(x)[2:]))*'0'+bin(x)[2:], data[:-1])))

    last_byte = bin(data[-1])[2:]

    result_binstr += last_byte
    return result_binstr


def writefile_bin(codeword_bin, filepath=OUTPUT_FILE):
    with open(filepath, 'wb') as fout:
        codeword_bytes = binstr_to_bytearray(codeword_bin)
        fout.write(codeword_bytes)

def readfile_bin(filepath):
    with open(filepath, 'rb') as fin:
        read_code = fin.read()
        read_codeword_binstr = bytearray_to_binstr(read_code)
    return read_codeword_binstr
if __name__ == "__main__":
    input_filepath = sys.argv[1]
    window_size = int(sys.argv[2])
    buffer_size = int(sys.argv[3])
    filetext = readfile_txt(filepath=input_filepath)

    codeword_binstr = encode(filetext, window_size, buffer_size,
                          write_to_file_path=input_filepath)

    writefile_bin(codeword_binstr)
    





