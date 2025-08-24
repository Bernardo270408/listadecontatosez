# Lista de Contatos (listadecontatosez)

Aplicação simples para gerenciar contatos, desenvolvida como trabalho escolar.  
Serve como exemplo prático de CRUD (Create, Read, Update, Delete) em Python com interface web.

---

## Funcionalidades
- Adicionar novo contato (nome, telefone, email, etc.)
- Listar todos os contatos cadastrados
- Buscar contatos por nome, email ou telefone
- Editar contato (em desenvolvimento)
- Excluir contato (em desenvolvimento)

---

## Tecnologias utilizadas
- Python — lógica principal
- HTML / CSS — interface web
- Flask — framework web para Python
- Bootstrap — estilização responsiva

---

## Estrutura do projeto
```

listadecontatosez/
│── app.py              # Arquivo principal da aplicação
│── requirements.txt    # Dependências do projeto
│── /templates          # Arquivos HTML (Jinja2)
│── /static             # CSS, JS e imagens

````

---

## Como rodar o projeto
1. Clone o repositório:
   ```bash
   git clone https://github.com/Bernardo270408/listadecontatosez.git
   cd listadecontatosez
   ````

2. (Opcional) Crie um ambiente virtual:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux / Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:

   ```bash
   pip install -r requirements.txt
   ```

4. Execute a aplicação:

   ```bash
   python app.py
   ```

5. Abra no navegador:

   ```
   http://127.0.0.1:5000
   ```

---

## Licença

Devido a natureza simples e academica, este projeto está sob a licença CC0 (Domínio Público).
Você pode usar, modificar e distribuir o código livremente.
