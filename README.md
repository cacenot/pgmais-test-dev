# Instruções de como executar

### Requerimentos

* Python 3.8

```sh
> pip3 install -r requirements.txt 
> python server.py
```

Fazer post na rota principal enviando um arquivo txt ou texto com o seguinte layout:

_IDMENSAGEM;DDD;CELULAR;OPERADORA;HORARIO_ENVIO;MENSAGEM_


```
http://0.0.0.0:8080/
```

# Instruções de como testar
```sh
> python -m unittest test
```

# O que utilizei para desenvolver

Linguagem: **Python 3.8**\
Sistema operacional: **Ubuntu**\
Editor de texto/IDE: **PyCharm**\
Libs
* Flask
* Requests