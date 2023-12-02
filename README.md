# basiC++

### Descrição

O basiC++ é um compilador desenvolvido para a linguagem de programação basiC++. Ele é capaz de analisar, interpretar e executar programas escritos em basiC++ com a extensão `.bpp`.

### Configuração do Ambiente

Para configurar o ambiente Python, siga as etapas abaixo:

1. Instale a última versão do Python a partir do [site oficial](https://www.python.org/downloads/).

2. Verifique a instalação executando o seguinte comando no terminal:

```bash
python --version
```

3. Instale as bibliotecas necessárias com o seguinte comando:

```bash
pip install -r requirements.txt
```

### Setup

Para configurar o projeto em sua máquina local, siga as etapas abaixo:

1. Clone o repositório:

```bash
git clone https://github.com/marcos-bah/basic-plus-plus.git
```

2. Navegue até o diretório do projeto:

```bash
cd basic-plus-plus
```

### Exemplo de Código

Aqui está um exemplo de como um programa em basiC++ pode parecer:

```cpp
start {
    function hello_world() {
        write("Hello, world!");
    }

    hello_world();
} end
```

Para compilar e executar este programa, você pode usar o seguinte comando:

```bash
python basic.py exemplo.bpp
```

# Uso do Makefile

Este projeto usa um Makefile para simplificar a execução do script `basic.py`. Para usar o Makefile, você precisa ter o `make` instalado no seu sistema.

## Executando o script `basic.py`

Para executar o script `basic.py` com um arquivo `.bpp`, use o seguinte comando:

```bash
make -B bpp caminho_relativo/nome_do_programa.bpp
```

### Executando Exemplos

Para executar os exemplos fornecidos, execute o seguinte comando:

```bash
make -B bpp samples/nome_do_exemplo.bpp
```
ou

```bash
python basic.py samples/nome_do_exemplo.bpp
```

Substitua `nome_do_exemplo.bpp` pelo nome do arquivo de exemplo que você deseja executar.

### Licença

Este projeto está licenciado sob a licença MIT.

### Contato

Se você tiver alguma dúvida ou sugestão, sinta-se à vontade para entrar em contato conosco.