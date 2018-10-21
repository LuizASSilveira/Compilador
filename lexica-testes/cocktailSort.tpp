inteiro: vet[10]
inteiro: tam
tam := 5

inteiro: temp1 

{ preenche o vetor no pior caso }
preencheVetor()
  inteiro: i
  inteiro: j
  i := 0
  j := tam
  repita
    vet[i] = j
    i := i + 1
    j := j - 1
  até i < tam
fim

cocktailSort()
	inteiro: i
	i := 0
	inteiro: j
	j := 0

	inteiro: passos
	passos := tam

	repita {while}
			repita{for 1}
					temp1 := i + 1
					se vet[i] > vet[temp1] então
	        			inteiro: temp
	        			temp 	   := vet[i]
	        			vet[i] 	   := vet[temp1]
	        			vet[temp1] := temp
	        		fim
			i++
			até i < tam -1 -j

			repita{for 2}
					i: tam-j
					temp1 := i - 1
					se vet[i] < vet[temp1] então
	        			inteiro: temp
	        			temp 	   := vet[i]
	        			vet[i] 	   := vet[temp1]
	        			vet[temp1] := temp
	        		fim
			i--
			até i > j
	até j < passos
fim		

inteiro principal()
  preencheVetor()
  cocktailSort()
  retorna(0)
fim