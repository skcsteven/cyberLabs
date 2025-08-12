# My First Steps on Windows - Reverse Engineering (3)

After downloading the program and running it with wine on linux, it looks to be a simple "enter a password" executable.

This is a windows PE file. First I decompile the program in ghidra and come across the entry() function:

'''

void entry(void)

{
  ___security_init_cookie(); # sets up canary cookie
  __scrt_common_main_seh(); # initialize the heap, I/O, global/static variables, and then call main() or WinMain(
  return;
}

'''

Within __scrt_common_main_seh() we need to find the call to the main function which will be relevant to solving this challenge.

After checking around and testing the function calls - forgive my lack of PE expertise - the main function is named FUN_00401d70.

Here is the main function decompiled in ghidra:

'''

void __fastcall main(undefined4 param_1)

{
  code *pcVar1;
  undefined4 ***pppuVar2;
  uint uVar3;
  int *piVar4;
  BOOL BVar5;
  HANDLE hProcess;
  undefined4 ****ppppuVar6;
  undefined4 extraout_ECX;
  undefined4 extraout_ECX_00;
  undefined4 uVar7;
  undefined4 extraout_ECX_01;
  uint uVar8;
  undefined4 extraout_ECX_02;
  char *pcVar9;
  UINT uExitCode;
  ushort local_34;
  undefined4 ***local_2c [4];
  undefined4 local_1c;
  uint local_18;
  uint local_14;
  void *local_10;
  undefined1 *puStack_c;
  undefined4 local_8;
  
  local_8 = 0xffffffff;
  puStack_c = &LAB_0041ca88;
  local_10 = ExceptionList;
  local_14 = DAT_0042b068 ^ (uint)&stack0xfffffffc;
  ExceptionList = &local_10;
  piVar4 = FUN_00402800(param_1,"Let\'s start with something easy!");
  FUN_00402ab0(piVar4);
  BVar5 = IsDebuggerPresent();
  uVar7 = extraout_ECX;
  if (BVar5 != 0) {
    piVar4 = FUN_00402800(extraout_ECX,"Ohnoes, debuggers are not allowed!");
    FUN_00402ab0(piVar4);
    uExitCode = 1;
    hProcess = GetCurrentProcess();
    TerminateProcess(hProcess,uExitCode);
    uVar7 = extraout_ECX_00;
  }
  FUN_00402800(uVar7,"Please enter your password\n> ");
  local_1c = 0;
  local_18 = 0xf;
  local_2c[0] = (undefined4 ***)((uint)local_2c[0] & 0xffffff00);
  local_8 = 0;
  FUN_00402b50(extraout_ECX_01,local_2c);
  uVar3 = local_18;
  pppuVar2 = local_2c[0];
  uVar8 = 0;
  local_34 = 0;
  do {
    ppppuVar6 = local_2c;
    if (0xf < local_18) {
      ppppuVar6 = (undefined4 ****)local_2c[0];
    }
    local_34 = local_34 |
               CONCAT11(*(undefined1 *)((int)ProcessEnvironmentBlock + 2),
                        *(byte *)((int)ppppuVar6 + uVar8) ^ (&DAT_00428684)[uVar8] ^
                        (&DAT_004286a8)[uVar8]);
    uVar8 = uVar8 + 1;
  } while (uVar8 < 0x21);
  pcVar9 = "Invalid password";
  if (local_34 == 0) {
    pcVar9 = "Correct password, use it as the flag";
  }
  piVar4 = FUN_00402800(uVar8,pcVar9);
  FUN_00402ab0(piVar4);
  piVar4 = FUN_00402800(extraout_ECX_02,"press [enter] to exit");
  FUN_00402ab0(piVar4);
  FUN_00401f50();
  if (0xf < uVar3) {
    ppppuVar6 = (undefined4 ****)pppuVar2;
    if (0xfff < uVar3 + 1) {
      ppppuVar6 = (undefined4 ****)pppuVar2[-1];
      if (0x1f < (uint)((int)pppuVar2 + (-4 - (int)ppppuVar6))) {
        FUN_0040a211();
        pcVar1 = (code *)swi(3);
        (*pcVar1)();
        return;
      }
    }
    FUN_0040585a(ppppuVar6);
  }
  ExceptionList = local_10;
  __security_check_cookie(local_14 ^ (uint)&stack0xfffffffc);
  return;
}

'''

From this, I extracted the relevant portion which takes our password input and xors it byte by byte with two predetermined arrays:

'''
  print(uVar7,"Please enter your password\n> ");
  local_1c = 0;
  inputLen = 0xf;
  userInput[0] = (undefined4 ***)((uint)userInput[0] & 0xffffff00);
  local_8 = 0;
  readUserInput(extraout_ECX_01,userInput);
  uVar3 = inputLen;
  pppuVar2 = userInput[0];
  counter = 0;
  local_34 = 0;
  do {
    ppppuVar6 = userInput;
    if (0xf < inputLen) {
      ppppuVar6 = (undefined4 ****)userInput[0];
    }
    local_34 = local_34 |
               CONCAT11(*(undefined1 *)((int)ProcessEnvironmentBlock + 2),
                        *(byte *)((int)ppppuVar6 + counter) ^ (&DAT_00428684)[counter] ^
                        (&DAT_004286a8)[counter]);
    counter = counter + 1;
  } while (counter < 0x21);
  pcVar8 = "Invalid password";
  if (local_34 == 0) {
    pcVar8 = "Correct password, use it as the flag";
'''

To get the password I used the following python code to perform the reverse xor-ing:
 
'''
key1 = bytes([
    0xEE, 0x81, more bytes here
])

key2 = bytes([
    0xB9, 0xB2, more bytes here
])

password_bytes = bytes([b1 ^ b2 for b1, b2 in zip(key1, key2)])
print(password_bytes.decode('ascii', errors='replace'))

'''
