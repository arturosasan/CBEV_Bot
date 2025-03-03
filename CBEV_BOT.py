from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, PollAnswerHandler
import logging
from datetime import datetime, time
import locale

# VERSION 1.1.0

# Habilitar los logs para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de Telegram
TOKEN = '7492611615:AAEumvRy9MM6peU7p1LABSKecbvAtJ4XNvE'

# Tu chat ID de Telegram (para recibir mensajes privados)
TU_CHAT_ID = 999999999

# Configurar la localización a español
locale.setlocale(locale.LC_TIME, 'spanish')

# Mensaje estándar de las encuestas
TXT = "RESPONDER ANTES DE LAS 18H, MÍNIMO 8 PERSONAS PARA ENTRENAR"

# Diccionario para almacenar respuestas a encuestas
respuestas_encuesta = {}

# Variable global para almacenar el chat_id del grupo
group_chat_id = None

# Función para iniciar el bot y guardar el chat_id del grupo
async def start(update: Update, context: CallbackContext) -> None:
    global group_chat_id
    group_chat_id = update.message.chat_id  # Guardar el chat_id del grupo
    await update.message.reply_text("Bot Iniciado. Hola! Estoy programado para mandar las encuestas de entrenamiento, cada lunes y miércoles a las 8 AM enviaré dichas encuestas, si por un casual no funcionan, escribid el comando /MON o /WEN para enviarlas manualmente. Para los partidos teneis que poner /JORN_['A' o 'B']_[nº de la Jornada]. IMPORTANTE, MANDAD SOLO UN COMANDO/ENCUESTA PARA EVITAR CONFUSIONES. Cualquier duda escribir por privado a @Arturitown, y si alguien quiere contribuir a mi desarrollo teneis el repositorio público de GitHub aquí : https://github.com/arturosasan/CBEV_Bot ¡UN, DOS, TRES, ELISEO/ENRIQUE!🏀")

# Función para enviar encuestas de entrenamiento
async def enviar_encuesta_entrenamiento(update: Update, context: CallbackContext, dia_semana: str) -> None:
    chat_id = group_chat_id if group_chat_id else TU_CHAT_ID
    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B").upper()
    mensaje = f"Entrenamiento {dia_semana} {dia} de {mes} a las 21 horas."
    ubicacion = "FUERA" if dia_semana == "LUNES" else "PABELLÓN"
    opciones = ["Sí", "No", "Entrenador"]
    encuesta_texto = f"{mensaje} {ubicacion}\n\n{TXT}"
    await context.bot.send_poll(chat_id=chat_id, question=encuesta_texto, options=opciones, is_anonymous=False)

async def enviar_MON(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(update, context, "LUNES")

async def enviar_WEN(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(update, context, "MIÉRCOLES")

# Función genérica para enviar encuestas de jornadas
async def enviar_JORNADA(update: Update, context: CallbackContext, equipo: str, jornada: int, fecha: str, rival: str, hora: str, encuentro: str) -> None:
    opciones = ["Sí", "No", "Disponible", "Entrenador"]
    encuesta_texto = f"Partido LIGA {fecha} vs {rival}, a las {hora}, {encuentro}"
    await context.bot.send_poll(chat_id=update.message.chat_id, question=encuesta_texto, options=opciones, is_anonymous=False)

# Handlers para jornadas del equipo A
async def enviar_JORN_A_17(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 17, "Domingo 9 de Marzo", "CUYABROS", "16:00", "quedamos 15:30")

async def enviar_JORN_A_18(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 18, "Domingo 23 de Marzo", "SPLASH", "18:00", "quedamos 17:30")

async def enviar_JORN_A_19(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 19, "Sábado 29 de Marzo", "FULL EQUIP", "18:00", "quedamos 17:30")

async def enviar_JORN_A_20(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 20, "Domingo 6 de Abril", "CLUB BASKET NORD", "18:00", "quedamos 17:30")

async def enviar_JORN_A_21(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 21, "Viernes 10 de Abril", "VALENCIA VETERANS", "20:45", "quedamos 20:15")

async def enviar_JORN_A_22(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 22, "Sábado 11 de Abril", "MANCHESTER FITI", "18:00", "quedamos 17:30")

# Handlers para jornadas del equipo B
async def enviar_JORN_B_17(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 17, "Domingo 9 de Marzo", "C.B. Descansados", "12:45", "quedamos 12:15")

async def enviar_JORN_B_18(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 18, "Domingo 23 de Marzo", "VIAJES GLOBUS XULOPLASTIKA", "20:00", "quedamos 19:30")

async def enviar_JORN_B_19(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 19, "Sábado 29 de Marzo", "MACCABI DE LEVANTAR", "19:00", "quedamos 18:30")

async def enviar_JORN_B_20(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 20, "Domingo 6 de Abril", "NA ROVELLA SPARTANS", "20:00", "quedamos 19:30")

async def enviar_JORN_B_21(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 21, "Domingo 27 de Abril", "FIVI", "18:00", "quedamos 17:30")

async def enviar_JORN_B_22(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 22, "Domingo 11 de Mayo", "BARRABAJA I", "20:00", "quedamos 19:30")

# Configurar el bot y el programador
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("MON", enviar_MON))
    application.add_handler(CommandHandler("WEN", enviar_WEN))
    application.add_handler(CommandHandler("JORN_A_17", enviar_JORN_A_17))
    application.add_handler(CommandHandler("JORN_A_18", enviar_JORN_A_18))
    application.add_handler(CommandHandler("JORN_A_19", enviar_JORN_A_19))
    application.add_handler(CommandHandler("JORN_A_20", enviar_JORN_A_20))
    application.add_handler(CommandHandler("JORN_A_21", enviar_JORN_A_21))
    application.add_handler(CommandHandler("JORN_A_22", enviar_JORN_A_22))
    application.add_handler(CommandHandler("JORN_B_17", enviar_JORN_B_17))
    application.add_handler(CommandHandler("JORN_B_18", enviar_JORN_B_18))
    application.add_handler(CommandHandler("JORN_B_19", enviar_JORN_B_19))
    application.add_handler(CommandHandler("JORN_B_20", enviar_JORN_B_20))
    application.add_handler(CommandHandler("JORN_B_21", enviar_JORN_B_21))
    application.add_handler(CommandHandler("JORN_B_22", enviar_JORN_B_22))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
