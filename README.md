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
python automata.py                            # Mapa vazio
python automata.py nome_do_arquivo.txt        # Carrega arquivo pré definido
```

### 🎯 Teste a demonstração
1. **Pressione 'D'** ou clique **"Demo"** para criar padrão exemplo
2. **Pressione Espaço** ou clique **"Play/Pause"** para iniciar

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
- **#** (amarelo) - **Condutor**
- **H** (azul) - **Cabeça de Elétron**
- **t** (vermelho) - **Cauda de Elétron**

## 📁 Formato de Arquivo
```
. # H t    <- Caracteres válidos
0 1 2 3    <- Ou números
```

Exemplo de arquivo válido pode ser encontrado em 'teste.txt', assim como executado com:
```
python main.py test.txt
```

## 📋 Requisitos
```bash
pip install pygame
```
