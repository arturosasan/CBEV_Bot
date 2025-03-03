from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext
import logging
from datetime import datetime, time, timezone, timedelta
import locale

# VERSION 1.1.0

# Habilitar los logs para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de Telegram
TOKEN = ''

# ID del chat donde se reenviarán las respuestas
TU_CHAT_ID = 0

# Variable global para almacenar el chat_id del grupo
GROUP_CHAT_ID = None

# Configurar la localización a español
locale.setlocale(locale.LC_TIME, 'spanish')

# Mensaje estándar de las encuestas
TXT = "RESPONDER ANTES DE LAS 18H, MÍNIMO 8 PERSONAS PARA ENTRENAR"

# Función para enviar encuestas de entrenamiento solo al grupo autorizado
async def enviar_encuesta_entrenamiento(context: CallbackContext, dia_semana: str) -> None:
    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B").upper()
    mensaje = f"Entrenamiento {dia_semana} {dia} de {mes} a las 21 horas."
    ubicacion = "FUERA" if dia_semana == "LUNES" else "PABELLÓN"
    opciones = ["Sí", "No", "Entrenador"]
    encuesta_texto = f"{mensaje} {ubicacion}\n\n{TXT}"
    await context.bot.send_poll(chat_id=GROUP_CHAT_ID, question=encuesta_texto, options=opciones, is_anonymous=False)

 # Función para manejar respuestas a encuestas
async def recibir_respuesta(update: Update, context: CallbackContext) -> None:
    respuesta = update.poll_answer
    usuario_id = respuesta.user.id
    usuario_nombre = respuesta.user.first_name
    opcion_elegida = respuesta.option_ids[0]  # Obtener la primera opción seleccionada
    opciones = ["Sí", "No", "Disponible", "Entrenador"]
    respuesta_texto = opciones[opcion_elegida]
    
    # Enviar la respuesta al usuario dueño del bot (admin)
    await context.bot.send_message(chat_id=TU_CHAT_ID, text=f"{usuario_nombre} respondió: {respuesta_texto}")
# Comandos manuales para enviar encuestas
async def enviar_MON(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(context, "LUNES")
    

async def enviar_WEN(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(context, "MIÉRCOLES")

# Función genérica para enviar encuestas de jornadas
async def enviar_JORNADA(update: Update, context: CallbackContext, equipo: str, jornada: int, fecha: str, rival: str, hora: str, encuentro: str) -> None:
    opciones = ["Sí", "No", "Disponible", "Entrenador"]
    encuesta_texto = f"Partido LIGA {fecha} vs {rival}, a las {hora}, {encuentro}"
    poll_message = await context.bot.send_poll(chat_id=GROUP_CHAT_ID, question=encuesta_texto, options=opciones, is_anonymous=False)
    context.bot_data[poll_message.poll.id] = poll_message.chat.id

# Programar envíos automáticos
async def programar_encuestas(application: Application):
    job_queue = application.job_queue
    job_queue.run_daily(lambda context: enviar_encuesta_entrenamiento(context, "LUNES"), time=time(8, 0, tzinfo=timezone.utc), days=(0,))
    job_queue.run_daily(lambda context: enviar_encuesta_entrenamiento(context, "MIÉRCOLES"), time=time(8, 0, tzinfo=timezone.utc), days=(2,))

# Comando /start para iniciar el bot
async def start(update: Update, context: CallbackContext) -> None:
    global GROUP_CHAT_ID
    GROUP_CHAT_ID = update.message.chat_id  # Guardar el chat_id del grupo
    await update.message.reply_text("Bot Iniciado. Hola! Estoy programado para mandar las encuestas de entrenamiento, cada lunes y miércoles a las 8 AM enviaré dichas encuestas, si por un casual no funcionan, escribid el comando /MON o /WEN para enviarlas manualmente. Para los partidos teneis que poner /JORN_['A' o 'B']_[nº de la Jornada]. IMPORTANTE, MANDAD SOLO UN COMANDO/ENCUESTA PARA EVITAR CONFUSIONES. Cualquier duda escribir por privado a @Arturitown, y si alguien quiere contribuir a mi desarrollo teneis el repositorio público de GitHub aquí : https://github.com/arturosasan/CBEV_Bot ¡UN, DOS, TRES, ELISEO/ENRIQUE!🏀")

# Handlers para jornadas del equipo A
async def enviar_JORN_A_17(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 17, "Domingo 9 de Marzo", "CUYABROS", "16:00", "quedamos 15:30")

async def enviar_JORN_A_18(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 18, "Domingo 23 de Marzo", "SPLASH", "18:00", "quedamos 17:30")

async def enviar_JORN_A_19(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 19, "Sábado 29 de Marzo", "FULL EQUIP", "18:00", "quedamos 17:30")

async def enviar_JORN_A_20(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "A", 20, "Domingo 6 de Abril", "CLUB BASKET NORD", "18:00", "quedamos 17:30")

# Handlers para jornadas del equipo B
async def enviar_JORN_B_17(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 17, "Domingo 9 de Marzo", "C.B. Descansados", "12:45", "quedamos 12:15")

async def enviar_JORN_B_18(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 18, "Domingo 23 de Marzo", "VIAJES GLOBUS XULOPLASTIKA", "20:00", "quedamos 19:30")

async def enviar_JORN_B_19(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 19, "Sábado 29 de Marzo", "MACCABI DE LEVANTAR", "19:00", "quedamos 18:30")

async def enviar_JORN_B_20(update: Update, context: CallbackContext) -> None:
    await enviar_JORNADA(update, context, "B", 20, "Domingo 6 de Abril", "NA ROVELLA SPARTANS", "20:00", "quedamos 19:30")

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
    application.add_handler(CommandHandler("JORN_B_17", enviar_JORN_B_17))
    application.add_handler(CommandHandler("JORN_B_18", enviar_JORN_B_18))
    application.add_handler(CommandHandler("JORN_B_19", enviar_JORN_B_19))
    application.add_handler(CommandHandler("JORN_B_20", enviar_JORN_B_20))

    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()