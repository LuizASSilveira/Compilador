; ModuleID = "LUIZ2"
target triple = "unknown-unknown-unknown"
target datalayout = ""

declare float @"leiaF"() 

define i32 @"main"() 
{
entry:
  %"x" = alloca i32
  %"y" = alloca float
  store i32 0, i32* %"x"
  store float              0x0, float* %"y"
  %".4" = call float @"leiaF"()
  %".5" = fptosi float %".4" to i32
  store i32 %".5", i32* %"x"
  %".7" = call float @"leiaF"()
  store float %".7", float* %"y"
  %"principal#x" = load i32, i32* %"x"
  %".9" = call i32 @"escrevaInteiro"(i32 %"principal#x")
  %"principal#y" = load float, float* %"y"
  %".10" = call float @"escrevaFlutuante"(float %"principal#y")
  %"retorna" = alloca i32, align 4
  store i32 0, i32* %"retorna"
  br label %"exit"
exit:
  %"ret_temp" = load i32, i32* %"retorna", align 4
  ret i32 %"ret_temp"
}

declare i32 @"escrevaInteiro"(i32 %".1") 

declare float @"escrevaFlutuante"(float %".1") 
