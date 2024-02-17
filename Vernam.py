# Vernam

# bytes("text", encoding="cp850") -> bytes
# "text".encode('cp850', 'ignore') -> bytes
# bytes([65]).decode('cp850') -> 'A'

import sys, os, shutil

class Vernam:

	def __init__(self, header: bool = False) -> None:
		if header == True:
			self.header()

	def header(self) -> None:
		if sys.platform in ["linux", "darwin"]:
			os.system("clear")
		elif sys.platform == "win32":
			os.system("cls")
		if shutil.get_terminal_size()[0] > 78:
			for i in self.TITLE:
				print(i)
		else:
			print(f"\033[92mVernam\033[00m v{self.VERSION}")

	def encode(self, text: str) -> bytes:
		return bytes(text, encoding="cp850")
	
	def decode(self, bin: list[int]) -> str:
		return bytes(bin).decode("cp850")

	def text_to_binary(self, text: str) -> list[str]:
		# Retorna una lista de octetos en bits tipados a strings.
		binarys = []
		for i in self.encode(text):
			octet = bin(i)[2:]
			while len(octet) < 8:
				octet = "0"+octet
			binarys.append(octet)
		return binarys

	def iterate_key(self, key: list[str], text_length: int) -> list[str]:
		keys = []
		key_length = len(key)
		if key_length == 0:
			return self.iterate_key(["00000000"], text_length)
		count = 0
		for i in range(text_length):
			if count == key_length:
				count = 0
			keys.append(key[count])
			count += 1
		return keys

	def xor(self, a: list[str], b: list[str]) -> list[str]:
		result = []
		for x, y in zip(a, b):
			octet = "" 
			for i in range(8):
				octet = octet+str(int(x[i]) ^ int(y[i]))
			result.append(octet)
		return result

	def encrypt(self):
		text = self.text_to_binary(input("\n + Escribe el texto a cifrar: "))
		text_length = len(text)
		key = self.iterate_key(self.text_to_binary(input(" + Introduce la clave: ")), text_length)

		print("\n    Texto", end="  -->  ")
		for i in text:
			print(i, end=" ")
		print("\n    Clave", end="  -->  ")
		for i in key:
			print(i, end=" ")
		print("\n           XOR  ", end=("---------"*text_length)[1:])

		result = self.xor(text, key)
		print("\n                ",  end="\033[93m")
		for i in result:
			print(i, end=" ")
		print("\033[00m\n                ", end="")
			
		for i in result:
			position_character = int(i, 2)
			if position_character <= 31 or position_character == 127:
				print(self.CONTROL_CHARACTERS[position_character], end=" ")
			else:
				print(self.decode([position_character]), end=" ")
		print()

	CONTROL_CHARACTERS: list[str] = ["NULL", "SOH", "STX", "ETX", "EOT", "ENQ", "ACK", "BEL", "BS", "HT", "LF", "VT", "FF", "CR", "SO", "SI", "DLE", "DC1", "DC2", "DC3", "DC4", "NAK", "SYN", "ETB", "CAN", "EM", "SUB", "ESC", "FS", "GS", "RS", "US", "DEL"]
	VERSION = "1.0.0"
	TITLE = [
		"+----------------------------------------------------------------------------+",
		"|                                                                            |",
		"|  \033[92moooooo     oooo\033[00m                                                           |",
		f"|   \033[92m`888.     .8'\033[00m {VERSION}                                                      |",
		"|    \033[92m`888.   .8'  .ooooo.  oooo d8b  ooo. .oo.   .oooo.   ooo. .oo.  .oo.\033[00m    |",
		"|     \033[92m`888. .8'  d88' `88b `888\"\"8P `888P\"Y88b  `P  )88b  `888P\"Y88bP\"Y88b\033[00m   |",
		"|      \033[92m`888.8'   888ooo888  888      888   888   .oP\"888   888   888   888\033[00m   |",
		"|       \033[92m`888'    888    .o  888      888   888  d8(  888   888   888   888\033[00m   |",
		"|        \033[92m`8'     `Y8bod8P' d888b    o888o o888o `Y8888\"8o o888o o888o o888o\033[00m  |",
		"|                                                                            |",
		"+----------------------------------------------------------------------------+"
	]

if __name__ == "__main__":
	obj = Vernam(header=True)
	try:
		while True:
			obj.encrypt()
	except KeyboardInterrupt:
		sys.exit("\nAdiós")