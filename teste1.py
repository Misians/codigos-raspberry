import serial
import time

# Configurações
DGUS_BAUD = 115200
# /dev/serial0 é a porta serial padrão nos pinos GPIO do Raspberry Pi
SERIAL_PORT = '/dev/serial0' 

def on_hmi_event(endereco, valor):
    """
    Equivalente ao onHMIEvent do Arduino.
    Chamado sempre que o display envia um comando de botão para o Raspberry.
    """
    print(f"OnEvent : [ Endereço VP: 0x{endereco:04X} | Valor Recebido: {valor} ]")
    
    if endereco == 0x1002:
        print("-> Executando ação customizada para o botão 1002!")

def set_page(ser, page_id):
    """
    Equivalente ao hmi.setPage()
    Endereço padrão de controle de sistema no DGUS II é 0x0084 ou 0x0014.
    """
    page_h = (page_id >> 8) & 0xFF
    page_l = page_id & 0xFF
    
    comando = bytearray([0x5A, 0xA5, 0x07, 0x82, 0x00, 0x84, 0x5A, 0x01, page_h, page_l])
    ser.write(comando)
    print(f"Comando enviado: Mudar para a Página {page_id}")

def listen(ser):
    """
    Equivalente ao hmi.listen() do Arduino.
    Fica varrendo o buffer para ver se a tela mandou algo.
    """
    if ser.in_waiting >= 9: 
        if ser.read(1)[0] == 0x5A:    
            if ser.read(1)[0] == 0xA5: 
                
                tamanho = ser.read(1)[0]
                comando = ser.read(1)[0]
                
                if comando == 0x83: 
                    vp_h = ser.read(1)[0]
                    vp_l = ser.read(1)[0]
                    data_len = ser.read(1)[0]
                    val_h = ser.read(1)[0]
                    val_l = ser.read(1)[0]
                    
                    endereco = (vp_h << 8) | vp_l
                    valor = (val_h << 8) | val_l
                    
                    on_hmi_event(endereco, valor)
                    
                    ser.reset_input_buffer()

def main():
    try:
        ser = serial.Serial(SERIAL_PORT, baudrate=DGUS_BAUD, timeout=0.1)
        
        # --- Equivalente ao setup() do Arduino ---
        print("DWIN HMI ~ Hello World (Raspberry Pi)")
        
        # Muda para a página 1 logo ao iniciar
        set_page(ser, 1)
        
        print("Escutando eventos do display... (Pressione Ctrl+C para sair)")
        
        # --- Equivalente ao loop() do Arduino ---
        while True:
            listen(ser)
            time.sleep(0.01) # Pequeno delay para não travar a CPU
            
    except serial.SerialException as e:
        print(f"Erro na porta serial: {e}")
        print("Dica: Use 'sudo python3 dwin_hello.py' se for erro de permissão.")
    except KeyboardInterrupt:
        print("\nPrograma encerrado pelo usuário.")
        if 'ser' in locals() and ser.is_open:
            ser.close()

if __name__ == "__main__":
    main()