# Como transformar seu script `.command` em um aplicativo (.app) ou executável no macOS

## 1. Transformar o .command em um .app usando o Automator

1. Abra o **Automator** (aplicativo nativo do macOS).
2. Clique em **Novo Documento** e selecione **Aplicativo**.
3. No campo de busca, digite **Shell** e arraste a ação **Executar Shell Script** para o fluxo de trabalho.
4. No campo do script, coloque o caminho para o seu `.command`, por exemplo:
   ```bash
   /caminho/para/seu/script/vnc-tunnel.command
   ```
   Ou, para garantir que o script seja executável:
   ```bash
   chmod +x /caminho/para/seu/script/vnc-tunnel.command
   /caminho/para/seu/script/vnc-tunnel.command
   ```
5. Salve o aplicativo com o nome desejado (ex: `VNC Tunnel.app`).
6. Agora você pode dar dois cliques no `.app` para rodar seu script.

---

## 2. Usar o Platypus para criar um .app

O [Platypus](https://sveinbjorn.org/platypus) é uma ferramenta gratuita que permite criar aplicativos `.app` a partir de scripts.

**Passos:**
1. Baixe e instale o Platypus.
2. Abra o Platypus e selecione seu script `.command` como script de entrada.
3. Configure o nome, ícone e outras opções conforme desejar.
4. Clique em **Create App**.
5. Pronto! Seu `.app` estará disponível para ser executado como um aplicativo normal do macOS.

---

## 3. Tornar o .command executável no Terminal

Se quiser apenas um executável de terminal (sem interface gráfica):

1. Dê permissão de execução ao script:
   ```bash
   chmod +x vnc-tunnel.command
   ```
2. Execute no terminal:
   ```bash
   ./vnc-tunnel.command
   ```

---

## Dicas Extras

- Certifique-se de que o script tenha permissão de execução (`chmod +x`).
- Se o script depende de caminhos relativos, prefira usar caminhos absolutos ou garanta que o diretório de trabalho esteja correto.
- O Platypus permite personalizar ícone, nome e até criar um app com interface gráfica simples.

---

Se precisar de um passo a passo detalhado ou de exemplos prontos, consulte este arquivo ou peça ajuda! 