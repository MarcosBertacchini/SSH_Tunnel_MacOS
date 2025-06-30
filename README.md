# SSH Tunnel MacOS

Este projeto tem como objetivo facilitar a criação de túneis SSH para acesso remoto seguro, especialmente útil para conexões VNC ou outros serviços em redes protegidas.

## Objetivo
Automatizar a criação de túneis SSH para acesso remoto, tornando o processo simples e acessível para usuários de MacOS (mas o script pode ser adaptado para outros sistemas).

## Funcionalidades
- Criação de túnel SSH para redirecionamento de portas
- Log de conexões
- Script fácil de usar

## Requisitos
- Python 3.x
- Acesso a um servidor SSH
- (Opcional) Terminal no MacOS ou Windows

## Como usar
1. Clone este repositório:
   ```sh
   git clone https://github.com/MarcosBertacchini/SSH_Tunnel_MacOS.git
   cd SSH_Tunnel_MacOS/ssh_Tunnel_app
   ```
2. Instale o Python, se necessário.
3. Execute o script principal:
   ```sh
   python ssh_Tunnel_v2.py
   ```
4. Siga as instruções exibidas no terminal para configurar o túnel SSH.

## Estrutura dos arquivos
- `ssh_Tunnel_v2.py`: Script principal para criar o túnel SSH
- `vnc_tunnel_log.txt`: Log das conexões realizadas
- `vnc-tunnel.command`: Script de automação para MacOS
- `Como_transformar_em_app_macOS.md`: Dicas para transformar o script em app no MacOS

## Contribuição
Pull requests são bem-vindos! Para mudanças maiores, por favor abra uma issue primeiro para discutir o que você gostaria de mudar.

## Licença
Este projeto está sob a licença MIT. 