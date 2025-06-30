#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Script SSH Tunnel VNC para MacMini 10.10
=========================================

Este script estabelece um túnel SSH para conectar via VNC a uma máquina Windows
através de um servidor intermediário (MacMini).

Funcionalidades:
- Cria túnel SSH com encaminhamento de porta
- Abre cliente VNC nativo do macOS
- Insere senha automaticamente via AppleScript
- Registra logs de conexão
- Tratamento robusto de erros
- Verificações de conectividade

Autor: Marcos Paulo Bertacchini
Versão: 2.0
Compatibilidade: macOS 10.10+ com Python 2.7
"""

import subprocess
import sys
import os
import time
import datetime
import socket
import signal
import threading

def registra_logip(ip):
	"""
	Função para registrar o IP do servidor intermediário no arquivo de log
	
	Args:
		ip (str): Endereço IP do servidor intermediário
		
	O arquivo de log é salvo em ~/Desktop/ssh_Tunnel/vnc_tunnel_log.txt
	com permissões 600 (apenas leitura/escrita para o proprietário)
	"""
	try:
		# Define o diretório de log na área de trabalho do usuário
		LOG_DIR = os.path.expanduser("~/Desktop/ssh_Tunnel")
		LOG_FILE = os.path.join(LOG_DIR, "vnc_tunnel_log.txt")
		
		# Cria o diretório se não existir
		if not os.path.exists(LOG_DIR):
			os.makedirs(LOG_DIR)
		
		# Abre o arquivo de log em modo append e adiciona entrada com timestamp
		with open(LOG_FILE, "a") as f:
			timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
			f.write("%s - %s\n" % (timestamp, ip))
		
		# Define permissões de segurança (apenas proprietário pode ler/escrever)
		os.chmod(LOG_FILE, 0o600)
		print("IP registrado no log: %s" % ip)
		
	except Exception as e:
		print("Erro ao registrar log: %s" % str(e))

def verificar_conectividade(host, port, timeout=5):
	"""
	Verifica se um host e porta estão acessíveis através de conexão TCP
	
	Args:
		host (str): Endereço IP ou hostname do servidor
		port (int): Número da porta a ser testada
		timeout (int): Tempo limite em segundos para a conexão
		
	Returns:
		bool: True se a conexão for bem-sucedida, False caso contrário
	"""
	try:
		# Cria socket TCP/IP
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(timeout)
		
		# Tenta conectar ao host:porta
		result = sock.connect_ex((host, port))
		sock.close()
		
		return result == 0
		
	except Exception as e:
		print("Erro ao verificar conectividade com %s:%s - %s" % (host, port, str(e)))
		return False

def verificar_ssh_disponivel():
	"""
	Verifica se o comando SSH está disponível no sistema
	
	Returns:
		bool: True se SSH estiver disponível, False caso contrário
	"""
	try:
		# Usa 'which' para localizar o executável SSH
		result = subprocess.call(["which", "ssh"], 
								stdout=subprocess.PIPE, 
								stderr=subprocess.PIPE)
		return result == 0
	except:
		return False

def verificar_vnc_disponivel():
	"""
	Verifica se o comando 'open' (cliente VNC nativo do macOS) está disponível
	
	Returns:
		bool: True se o cliente VNC estiver disponível, False caso contrário
	"""
	try:
		# Verifica se o comando 'open' está disponível
		result = subprocess.call(["which", "open"], 
								stdout=subprocess.PIPE, 
								stderr=subprocess.PIPE)
		return result == 0
	except:
		return False

def timeout_handler(signum, frame):
	"""
	Handler para timeout da conexão SSH (não utilizado atualmente)
	
	Args:
		signum: Sinal recebido
		frame: Frame atual da execução
		
	Raises:
		Exception: Timeout na conexão SSH
	"""
	raise Exception("Timeout na conexão SSH")

# =============================================================================
# CONFIGURAÇÕES DO SISTEMA
# =============================================================================

LOCAL_PORT = 5901			# Porta local para redirecionamento do túnel
WIN_IP = "169.254.1.20"		# Endereço IP da máquina Windows de destino
WIN_VNC_PORT = 5900			# Porta VNC padrão na máquina Windows
MACMINI_USER = "gdlocal"	# Usuário para login no servidor intermediário
VNCP = "123123"				# Senha VNC da máquina Windows
SSH_TIMEOUT = 30			# Timeout para conexão SSH em segundos

def main():
	"""
	Função principal que executa todo o fluxo do túnel SSH/VNC
	
	Fluxo de execução:
	1. Verifica dependências do sistema
	2. Valida disponibilidade da porta local
	3. Solicita IP do servidor intermediário
	4. Testa conectividade com servidor intermediário
	5. Estabelece túnel SSH
	6. Abre cliente VNC
	7. Insere senha automaticamente
	8. Registra log da conexão
	9. Aguarda encerramento pelo usuário
	"""
	
	# =============================================================================
	# VERIFICAÇÕES INICIAIS DO SISTEMA
	# =============================================================================
	print("Verificando dependências do sistema...")
	
	# Verifica se SSH está disponível
	if not verificar_ssh_disponivel():
		print("Erro: SSH não está disponível no sistema.")
		print("Certifique-se de que o OpenSSH está instalado.")
		sys.exit(1)
	
	# Verifica se cliente VNC está disponível
	if not verificar_vnc_disponivel():
		print("Erro: Cliente VNC não está disponível no sistema.")
		print("Certifique-se de que está executando no macOS.")
		sys.exit(1)
	
	# Verifica se a porta local está disponível (não em uso)
	if verificar_conectividade("localhost", LOCAL_PORT, 1):
		print("Erro: Porta %d já está em uso por outro processo." % LOCAL_PORT)
		print("Encerre o processo que está usando esta porta ou altere LOCAL_PORT.")
		sys.exit(1)
	
	# =============================================================================
	# ENTRADA DE DADOS DO USUÁRIO
	# =============================================================================
	MACMINI_IP = raw_input("Digite o IP do servidor intermediário: ").strip()
	if not MACMINI_IP:
		print("Erro: IP deve ser digitado.")
		sys.exit(1)
	
	# =============================================================================
	# VERIFICAÇÃO DE CONECTIVIDADE
	# =============================================================================
	print("Verificando conectividade com o servidor intermediário...")
	if not verificar_conectividade(MACMINI_IP, 22, 10):
		print("Erro: Não foi possível conectar ao servidor intermediário %s na porta 22" % MACMINI_IP)
		print("Verifique:")
		print("  - Se o IP está correto")
		print("  - Se o servidor está ligado e acessível")
		print("  - Se o SSH está rodando na porta 22")
		print("  - Se há conectividade de rede")
		sys.exit(1)
	
	# =============================================================================
	# CONSTRUÇÃO DO COMANDO SSH
	# =============================================================================
	ssh_command = [
		"ssh",															# Comando SSH
		"-N", 															# Modo não-interativo (apenas túnel)
		"-o", "ConnectTimeout=%d" % SSH_TIMEOUT,						# Timeout de conexão
		"-o", "ServerAliveInterval=60",									# Envia keep-alive a cada 60s
		"-o", "ServerAliveCountMax=3",									# Máximo 3 tentativas de keep-alive
		"-L", "{0}:{1}:{2}".format(LOCAL_PORT, WIN_IP, WIN_VNC_PORT),	# Encaminhamento de porta local
		"{0}@{1}".format(MACMINI_USER, MACMINI_IP)						# Login no servidor intermediário
	]

	# =============================================================================
	# ESTABELECIMENTO DO TÚNEL SSH
	# =============================================================================
	print("\nIniciando túnel SSH...")
	try:
		# Inicia o processo SSH em background
		ssh_proc = subprocess.Popen(
			ssh_command,
			stdin=subprocess.PIPE,		# Redireciona entrada padrão
			stdout=subprocess.PIPE,		# Captura saída padrão
			stderr=subprocess.PIPE		# Captura saída de erro
		)
		
		# Aguarda 3 segundos e verifica se o processo ainda está rodando
		time.sleep(3)
		if ssh_proc.poll() is not None:
			# Processo terminou prematuramente - captura erros
			stdout, stderr = ssh_proc.communicate()
			print("Erro ao iniciar túnel SSH:")
			if stderr:
				print("Erro: %s" % stderr)
			sys.exit(1)
		
		# Aguarda mais 5 segundos para o túnel se estabelecer completamente
		time.sleep(5)
		
		# Verifica se o túnel está funcionando testando a porta local
		if not verificar_conectividade("localhost", LOCAL_PORT, 5):
			print("Erro: Túnel SSH não foi estabelecido corretamente.")
			print("Verifique as credenciais e permissões de acesso.")
			ssh_proc.terminate()
			sys.exit(1)
		
		print("Túnel SSH estabelecido com sucesso!")
		print("Porta local %d -> %s:%d" % (LOCAL_PORT, WIN_IP, WIN_VNC_PORT))
		
	except Exception as e:
		print("Erro ao iniciar túnel SSH: %s" % str(e))
		sys.exit(1)

	# =============================================================================
	# ABERTURA DO CLIENTE VNC
	# =============================================================================
	vnc_url = "vnc://localhost:{0}".format(LOCAL_PORT)
	print("Abrindo cliente VNC...")
	print("URL VNC: %s" % vnc_url)
	
	try:
		# Abre o cliente VNC nativo do macOS
		subprocess.call(["open", vnc_url])
	except Exception as e:
		print("Erro ao abrir cliente VNC: %s" % str(e))
		print("Tente abrir manualmente: %s" % vnc_url)
		ssh_proc.terminate()
		sys.exit(1)

	# Aguarda 2 segundos para a janela VNC aparecer
	time.sleep(2)

	# =============================================================================
	# INSERÇÃO AUTOMÁTICA DE SENHA
	# =============================================================================
	print("Inserindo senha automaticamente...")

	# Script AppleScript para inserir senha e confirmar
	osascript_code = '''
	tell application "System Events"
		keystroke "{}"
		keystroke return
		-- Alternativa: Clicar no botão "Connect"
		-- delay 0.5
		-- click button "Connect" of windows 1 of process "ScreenSharingAgent"
	end tell
	'''.format(VNCP)

	try:
		# Executa o AppleScript para inserir a senha
		subprocess.call(["osascript", "-e", osascript_code])
		print("Senha inserida automaticamente.")
	except Exception as e:
		print("Erro ao inserir senha automaticamente: %s" % str(e))
		print("Por favor, insira a senha manualmente: %s" % VNCP)
		print("Dica: Verifique se o 'Acesso para Assistente' está habilitado em Preferências do Sistema > Segurança e Privacidade > Privacidade > Acessibilidade")

	# =============================================================================
	# REGISTRO DE LOG E FINALIZAÇÃO
	# =============================================================================
	registra_logip(MACMINI_IP)

	# =============================================================================
	# LOOP PRINCIPAL - AGUARDA ENCERRAMENTO
	# =============================================================================
	print("\n" + "="*50)
	print("TÚNEL SSH/VNC ATIVO")
	print("="*50)
	print("Para encerrar, pressione CTRL+C no terminal.")
	print("Conexão: %s -> %s:%d" % (MACMINI_IP, WIN_IP, WIN_VNC_PORT))
	print("="*50)
	
	try:
		# Aguarda o processo SSH terminar (loop infinito até CTRL+C)
		ssh_proc.wait()
		
	except KeyboardInterrupt:
		# Captura CTRL+C do usuário
		print("\nEncerrando túnel SSH...")
		
		try:
			# Tenta encerrar o processo graciosamente
			ssh_proc.terminate()
			ssh_proc.wait(timeout=5)		# Aguarda até 5 segundos
			
		except subprocess.TimeoutExpired:
			# Se não responder, força o encerramento
			print("Forçando encerramento do processo...")
			ssh_proc.kill()
			
		print("Conexão SSH encerrada.")
		
		# Tenta fechar a janela do terminal (opcional)
		try:
			subprocess.call(["osascript", "-e", 'tell application "Terminal" to close first windows'])
		except:
			pass  # Ignora erros ao fechar janela do terminal

if __name__ == "__main__":
	# Ponto de entrada do script
	main()

