from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext, PollAnswerHandler
import logging
from datetime import datetime, time
import locale

# Habilitar los logs para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Token del bot de Telegram
TOKEN = ''

# Tu chat ID de Telegram (para recibir mensajes privados)
TU_CHAT_ID = 99999999

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
    await update.message.reply_text("Bot iniciado. ¡Hola! Soy el bot de WTCBEV. Estoy configurado para enviar encuestas los lunes y miércoles a las 8 AM para los entrenamientos de la semana. Si por algún casual estas encuestas no se envían, puedes usar los comandos /MON y /WEN para enviarlas manualmente. ,Para enviar las encuestas de los partidos simplemente tienes que poner /JORN_['A' o 'B']_['nº de la jornada']. Esta versión del bot (1.1.1) solamente están las jornadas hasta la 22 (no aparecen más en Swish). IMPORTANTE, USAD SOLAMENTE UNA VEZ CADA COMANDO PARA EVITAR CONFUSIONES. ¡UN, DOS, TRES, ENRIQUE! 🏀")

# Función para enviar la encuesta del lunes
async def enviar_MON(update: Update, context: CallbackContext) -> None:
    chat_id = group_chat_id if group_chat_id else TU_CHAT_ID
    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B").upper()
    mensaje = f"Entrenamiento LUNES {dia} de {mes} a las 21 horas. FUERA"
    opciones = ["Sí", "No","Entrenador"]
    encuesta_texto = f"{mensaje}\n\n{TXT}"
    await context.bot.send_poll(chat_id=chat_id, question=encuesta_texto, options=opciones, is_anonymous=False)

# Función para enviar la encuesta del miércoles
async def enviar_WEN(update: Update, context: CallbackContext) -> None:
    chat_id = group_chat_id if group_chat_id else TU_CHAT_ID
    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B").upper()
    mensaje = f"Entrenamiento MIÉRCOLES {dia} de {mes} a las 21 horas. PABELLÓN"
    opciones = ["Sí", "No", "Entrenador"]
    encuesta_texto = f"{mensaje}\n\n{TXT}"
    await context.bot.send_poll(chat_id=chat_id, question=encuesta_texto, options=opciones, is_anonymous=False)

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

# Función para verificar respuestas a las 18:00
async def verificar_respuestas(context: CallbackContext) -> None:
    if respuestas_encuesta:
        total_si = sum(respuestas["sí"] for respuestas in respuestas_encuesta.values())
        mensaje = "Hay más de 8 personas para entrenar hoy" if total_si >= 8 else "Hay menos de 8 personas para entrenar"
        await context.bot.send_message(chat_id=TU_CHAT_ID, text=mensaje)
    else:
        await context.bot.send_message(chat_id=TU_CHAT_ID, text="No hay respuestas registradas para hoy.")


# Configurar el bot y el programador
def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
    # Comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("MON", enviar_MON))
    application.add_handler(CommandHandler("WEN", enviar_WEN))
    
    
    # Manejar respuestas de encuestas
    application.add_handler(PollAnswerHandler(recibir_respuesta))
    
    # Programar el envío de encuestas los lunes y miércoles a las 8 AM
    job_queue = application.job_queue
    job_queue.run_daily(enviar_MON, time=time(hour=8, minute=0), days=(0,))  # Lunes
    job_queue.run_daily(enviar_WEN, time=time(hour=8, minute=0), days=(2,))  # Miércoles
    job_queue.run_daily(verificar_respuestas, time=time(hour=18, minute=0))  # Verificar respuestas a las 18:00
    
    # Iniciar el bot
    application.run_polling()

if __name__ == '__main__':
    main()
