; ModuleID = "LUIZ2"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"leiaF"() 

define i32 @"daniel"() 
{
entry:
  %"jonas" = alloca i32
  store i32 23, i32* %"jonas"
exit:
}

define i32 @"main"() 
{
entry:
  %"retorna" = alloca i32, align 4
  store i32 10, i32* %"retorna"
  br label %"exit"
exit:
  %"ret_temp" = load i32, i32* %"retorna", align 4
  ret i32 %"ret_temp"
}
