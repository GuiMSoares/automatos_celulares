# WireWorld Cellular Automaton

Implementação completa do autômato celular WireWorld com interface gráfica.

## ✅ Funcionalidades Implementadas
- Autômato celular WireWorld completo
- Play/Pause da simulação
- Step (executa uma iteração)
- Reset (volta ao estado inicial) 
- Carregar/Salvar arquivos de texto
- Desenho e edição com mouse
- Ajuste de velocidade da simulação
- Interface gráfica com botões
- Padrão de demonstração automático

## 🚀 Como Usar

### Execução
```bash
python automata.py                    # Grade vazia
python automata.py arquivo.txt        # Carrega arquivo
```

### 🎯 Teste a demonstração
1. **Pressione 'D'** ou clique **"Demo"** para criar padrão exemplo
2. **Pressione Espaço** ou clique **"Play/Pause"** para iniciar
3. Veja os elétrons se movendo pelos fios!

## ⌨️ Controles

### Teclado
- **Espaço** - Play/Pause
- **N** - Step (uma iteração)
- **R** - Reset
- **D** - Criar padrão demo
- **L** - Carregar arquivo
- **S** - Salvar arquivo
- **1/2/3/4** - Pincéis: Vazio/Condutor/Cabeça/Cauda
- **+/-** - Velocidade
- **Esc** - Sair

### Mouse
- **Esquerdo** - Pintar com pincel atual
- **Direito** - Apagar (vazio)
- **Meio** - Alternar estado da célula

### Botões da Interface
- **Play/Pause** - Controla simulação
- **Step** - Uma iteração
- **Reset** - Estado inicial
- **Load/Save** - Arquivos
- **Speed +/-** - Velocidade
- **Demo** - Gera um exemplo de demonstração

## 🔌 Estados das Células
- **.** (cinza) - **Vazio**
- **#** (amarelo) - **Condutor** (fio)
- **H** (azul) - **Cabeça de Elétron**
- **t** (vermelho) - **Cauda de Elétron**

## 📁 Formato de Arquivo
```
. # H t    <- Caracteres válidos
0 1 2 3    <- Números também funcionam
```

**Arquivos de exemplo:** `test1.txt`, `test2.txt`

## 📋 Requisitos
```bash
pip install pygame
```
