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
- Demonstração de portas lógicas

## 🚀 Como Usar

### Execução
```bash
python main.py                            # Mapa vazio
python main.py nome_do_arquivo.txt        # Carrega arquivo pré definido do mesmo diretório
```

## ⌨️ Controles

### Teclado
- **Espaço** - Play/Pause
- **N** - Step (uma iteração)
- **R** - Reset
- **L** - Carregar arquivo
- **S** - Salvar arquivo
- **1/2/3/4** - Pincéis: Vazio/Condutor/Cabeça/Cauda
- **+/-** - Velocidade
- **Esc** - Sair

### Mouse
- **Esquerdo** - Pintar com pincel atual
- **Direito** - Apagar
- **Meio** - Alternar estado da célula

### Botões da Interface
- **Play/Pause** - Pausa ou continua a simulação
- **Step** - Uma iteração
- **Reset** - Estado inicial
- **Load/Save** - Carregar/salvar arquivo
- **Speed +/-** - Velocidade

## 🔌 Estados das Células
- **.** (cinza) - **Vazio**
- **#** (amarelo) - **Condutor**
- **H** (azul) - **Cabeça de Elétron**
- **t** (vermelho) - **Cauda de Elétron**

## 📁 Formato de Arquivo
```
. # H t    <- Caracteres válidos (H -> cabeça, t -> cauda, # -> caminho)
0 1 2 3    <- Ou números
```

Exemplos de arquivos de portas lógicas estão no diretório /gates e podem ser rodados com:
```bash
python main.py ../gates/gate-and.txt    # Para porta and
```

## 📋 Requisitos
```bash
pip install pygame
```
