import numpy as np
import random as rd
import math as ma

def softmax(u):
    max_u = max(u)
    exp_u = np.exp(u - max_u)
    return exp_u / np.sum(exp_u)

def d_softmax(u):
    return (1 if u > 0 else 0)

def sigmoide(u):
    return 1./(1+ma.exp(-u))

def d_sigmoide(u):
    return u*(1-u)

def relu(u):
    return max(0,u)
 
def ler_Arquivo(arquivo):
    atributos  = []
    classes    = []
    with open(arquivo,"r",encoding="utf-8") as arq:
        for linha in arq:
            linha = linha.strip()
            if linha == "":
                continue
            aux1 = linha.split()
            aux2 = [float(x) for x in aux1[:-1]]
            aux3 = aux1[-1]
            atributos.append(aux2)
            classes.append(int(aux3) - 1)
        return atributos, classes

def mlp_treino(nx,nz,ny,tempo,d,cl,alfa_input=0.01,ativacao_oculta="relu",ativacao_saida="softmax"):
   x = np.zeros(nx+1,float)
   y = np.zeros(ny,float)
   z = np.zeros(nz+1,float)
   dy = np.zeros(ny,float)
   dz = np.zeros(nz,float)
   #alfa = 0.4 # SIGMOIDE
   alfa = alfa_input # RELU/SOFTMAX
   
   # PASSO 0
   # PESOS - SIGMOIDE
   v = np.random.uniform(-1,1,(nx+1,nz))
   w = np.random.uniform(-1,1,(nz+1,ny))
   ns = len(d)
   # PASSO 1
   for t in range(tempo):
       # PASSO 2
       linha = rd.randrange(ns)
       # PASSO 3
       for i in range(nx):
           x[i] = d[linha][i]
       x[nx-1] = 1
       # saída esperada
       se = np.zeros(ny,int)
       se[cl[linha]] = 1
       # PASSOS 4 E 5
       u_z = np.zeros(nz)
       for j in range(nz):
           z[j] = 0
           for i in range(nx+1):
               u_z[j] += v[i][j]*x[i]
           if ativacao_oculta == "sigmoid":
               z[j] = sigmoide(u_z[j])
           else:
               z[j] = relu(u_z[j])
       z[nz-1] = 1
       if ativacao_saida == "sigmoid":
           # PASSOS 6, 7, 8 - SIGMOIDE
           sr = np.zeros(ny,int)
           for k in range(ny):
               y[k] = 0
               for j in range(nz+1):
                   y[k] += w[j][k]*z[j]
               y[k] = sigmoide(y[k])
               # PASSO 8 - saída da MLP    
               if y[k]>=0.5:
                   sr[k] = 1
       else:
           # PASSOS 6, 7, 8 - SOFTMAX
           u = np.zeros(ny)
           for k in range(ny):
               for j in range(nz+1):
                   u[k] += w[j][k]*z[j]
           y = softmax(u)
           # saída da rede
           sr = np.zeros(ny, int)
           classe_pred = np.argmax(y)
           sr[classe_pred] = 1
       
       # PASSO 9
       for k in range(ny):
           if ativacao_saida == "sigmoid":
               dy[k] = (se[k]-sr[k])*d_sigmoide(y[k])
           else:
               dy[k] = (se[k] - y[k])
      
       for j in range(nz):
           dz[j] = 0
           for k in range(ny):
               dz[j] += dy[k]*w[j][k]
               if ativacao_oculta == "sigmoid":
                   dz[j] = dz[j]*d_sigmoide(z[j])
               else:
                   dz[j] = dz[j] * d_softmax(u_z[j])
       
       for i in range(nx+1):
           for j in range(nz):
               v[i][j] += alfa*x[i]*dz[j]
       for j in range(nz+1):
           for k in range(ny):
               w[j][k] += alfa*z[j]*dy[k]
   return v,w


def mlp_teste(
    nx,
    nz,
    ny,
    ns,
    d,
    cl,
    v,
    w,
    ativacao_oculta="relu",
    ativacao_saida="softmax",
):
   x = np.zeros(nx+1,float)
   y = np.zeros(ny,float)
   z = np.zeros(nz+1,float)
   ac = 0
   
   # PASSO 1
   for linha in range(ns):
       # PASSO 3
       for i in range(nx):
           x[i] = d[linha][i]
       x[nx-1] = 1
       # saída esperada
       se = np.zeros(ny,int)
       se[cl[linha]] = 1
       # PASSOS 4 E 5
       for j in range(nz):
           z[j] = 0
           for i in range(nx+1):
               z[j] += v[i][j]*x[i]
           if ativacao_oculta == "sigmoid":
               z[j] = sigmoide(z[j])
           else:
               z[j] = relu(z[j])
       z[nz-1] = 1
       if ativacao_saida == "sigmoid":
           # PASSOS 6,7,8 - SIGMOIDE
           sr = np.zeros(ny,int)
           for k in range(ny):
               y[k] = 0
               for j in range(nz+1):
                   y[k] += w[j][k]*z[j]
               y[k] = sigmoide(y[k])
               if y[k]>=0.5:
                   sr[k] = 1
       else:
           u = np.zeros(ny)
           for k in range(ny):
               for j in range(nz+1):
                   u[k] += w[j][k]*z[j]
           y = softmax(u)
       
           # saída da rede
           sr = np.zeros(ny, int)
           classe_pred = np.argmax(y)
           sr[classe_pred] = 1

       acertou = True
       for k in range(ny):
           if se[k]!=sr[k]:
               acertou = False
               break
       if acertou:
           ac += 1
   return 100.*ac/ns

# MÓDULO PRINCIPAL
arquivo = "dados.data-numeric"
d,cl = ler_Arquivo(arquivo)

def normalizar_Dados(atributos):
    matriz = np.array(atributos)
    
    minimos = matriz.min(axis=0)
    maximos = matriz.max(axis=0)
    
    denominador = maximos - minimos
    denominador[denominador == 0] = 1    
    matriz_normalizada = (matriz - minimos) / denominador
    
    return matriz_normalizada.tolist()
    
d = normalizar_Dados(d)

tempo = 600
nx = len(d[0])
ny = len(set(cl))
n = 30

for nz in range(5,31):
    ac = 0
    for c in range(n):
        v, w = mlp_treino(nx,nz,ny,tempo,d,cl)
        #print("Pesos V: ",v)
        #print("Pesos W: ",w)
        ac += mlp_teste(nx,nz,ny,len(d),d,cl,v,w)
    print(f"NZ: {nz:02d} | Acurácia: {(ac/n):.2f}")
    
