# Orientação sobre a API Biblioteca

## Significado dos status code do servidor

1. "Ok", 200
   - resultado bem sucedido
   - obs.: pode ser retornado "Ok" ou o conteudo pedido
2. "Unauthorized", 401
   - o usuario não está cadastrado no sistema
3. "Forbidden", 403

   - o usuario não está cadastrado no sistema

4. "Not Acceptable", 406
5. "Conflict", 409

## Exemplos em Javascript

- relacionados aos usuarios

  ```js
  // modelo de usuario
  user = {
    books_ids: [],
    email: "email@email.com",
    id: 0,
    is_admin: true | false,
    name: "username",
    password: "****",
  };
  ```

  1. login

  ```js
  // para usuario e admin
  async function(){
    const data = new FormData();
    data.append("email", email);
    data.append("password", password);
    // configurações do post via fetch
    const options = {
      method: "POST",
      body: data,
    };
    result = await fetch(`${ApiUrl}/login`, options);
    // retornos:
    // "Ok", 200
    // "Unauthorized", 401

    /*<...>*/
  }
  ```

  1. logout

  ```js
  // para usuario e admin
  async function(){
    result = await fetch(`${ApiUrl}/logout`);
    // retornos:
    // "Ok", 200
    // "Unauthorized", 401

    /*<...>*/
  }
  ```

  3. cadastrar usuario

  ```js
  // somente para admin
  async function(){
    const data = new FormData();
    data.append("email", email);
    data.append("name", name);
    data.append("password", password);
    data.append("is_admin", is_admin);
    // configurações do post via fetch
    const options = {
      method: "POST",
      body: data,
    };
    result = await fetch(`${ApiUrl}/login`, options);
    // retornos:
    // "Ok", 200
    // "Unauthorized", 401
    // "Forbidden", 403
    // "Not Acceptable", 406
    // "Conflict", 409

    /*<...>*/
  }
  ```

  4. consultar usuarios

  ```js
  // somente para admin
  async function(){
    result = await fetch(`${ApiUrl}/users`);
    // [user,...], 200
    // "Unauthorized", 401
    // "Forbidden", 403

    /*<...>*/
  }
  ```

  5. consultar um unico usuario

  ```js
  // somente para admin
  async function(){
  result = await fetch(`${ApiUrl}/user/${id}`);
    // user, 200
    // "Unauthorized", 401
    // "Forbidden", 403

    /*<...>*/
  }
  ```

  6. consultar as proprias informações

  ```js
  // para usuario e admin
  async function(){
    result = await fetch(`${ApiUrl}/info/${id}`);
    // "Ok", 200
    // "Unauthorized", 401

    /*<...>*/
  }
  ```

- relacionados aos livros

  ```js
  // modelo de um livro
  book = {
    author: "name",
    file: ... // arquivo de imagem
    // link da imagem é : {api}/img/<isbn10>.<ext>
    // ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']
    cover: "", // link da 'capa' caso nâo envie o arquivo
    edition: "2020",
    isbn10: "a1b2c3d4",
    obs: "", // 'observação' opcional
    on_loan: true | false, // em emprestimo
    sub_title: "1234",
    title: "abcd",
    year: "2021"
  },
  ```

  1. consultar livros

  ```js
  // para usuario e admin
  async function(){
    result = await fetch(`${ApiUrl}/books`);
    // [book,...], 200
    // "Unauthorized", 401

    /*<...>*/
  }
  ```

  2. consultar um unico livro

  ```js
  // para usuario e admin
  async function(){
    result = await fetch(`${ApiUrl}/book/${isbn10}`);
    // book, 200
    // "Unauthorized", 401

    /*<...>*/
  }
  ```

  3. emprestimo

  ```js
  // para usuario e admin
  async function(){
    const data = new FormData();
    data.append("isbn10", isbn10);
    // configurações do post via fetch
    const options = {
      method: "POST",
      body: data,
    };
    result = await fetch(`${ApiUrl}/book/lending/${isbn10}`);
    // "Ok", 200
    // "Unauthorized", 401
    // "Conflict", 409

    /*<...>*/
  }
  ```

  4. adicionar livro

  ```js
  // somente para admin
  async function(){
    const data = new FormData();
    data.append("isbn10", isbn10);
    data.append("title", title);
    data.append("cover", cover); // 'capa' se for opcional, cover=""
    data.append("sub_title", subTitle);
    data.append("obs", obs); // se for opcional, obs=""
    data.append("author", author);
    data.append("edition", edition);
    data.append("year", year);
    // configurações do post via fetch
    const options = {
      method: "POST",
      body: data,
    };
    result = await fetch(`${ApiUrl}/login`, options);
    // "Ok", 200
    // "Unauthorized", 401
    // "Forbidden", 403
    // "Conflict", 409

    /*<...>*/
  }
  ```

  5. editar livro

  ```js
  // somente para admin
  async function(){
    const data = new FormData();
    /*
    // igual ao adicionar, só que todas os campos são opcionais
    */
    // configurações do post via fetch
    const options = {
      method: "POST",
      body: data,
    };
    result = await fetch(`${ApiUrl}/login`, options);
    // "Ok", 200
    // "Unauthorized", 401
    // "Forbidden", 403
    // "Conflict", 409

    /*<...>*/
  }
  ```
