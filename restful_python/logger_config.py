import logging

# Configuração Global do Logger
def setup_logger():
    logger = logging.getLogger("MinhaAplicacao")  # Nome global para o logger
    logger.setLevel(logging.DEBUG)  # Define o nível global de log

    # Handler para console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # Handler para arquivo
    file_handler = logging.FileHandler("app.log")
    file_handler.setLevel(logging.DEBUG)

    # Formato dos logs
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Adicionando os handlers ao logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger


# Configurando o logger global
logger = setup_logger()
