from telegram import Update
from telegram.ext import Application, CommandHandler, PollAnswerHandler, CallbackContext, JobQueue
import logging
from datetime import datetime, time, timezone
import locale
import os
from dotenv import load_dotenv

# VERSION 1.2 

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener valores del .env
TOKEN = os.getenv("TOKEN")
TU_CHAT_ID = int(os.getenv("CHAT_ID"))  # Convertir a entero porque los IDs son números

# Variables globales
GROUP_CHAT_ID = None
respuestas_si = 0

# Habilitar los logs para depuración
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Configurar la localización a español
locale.setlocale(locale.LC_TIME, 'spanish')

# Mensaje estándar de las encuestas
TXT = "RESPONDER ANTES DE LAS 18H, MÍNIMO 8 PERSONAS PARA ENTRENAR"

async def enviar_encuesta_entrenamiento(context: CallbackContext, dia_semana: str) -> None:
    global respuestas_si
    respuestas_si = 0  # Reiniciar el contador en cada nueva encuesta

    if GROUP_CHAT_ID is None:
        logger.warning("El chat del grupo no está configurado. Usa /start en el grupo primero.")
        return

    fecha_actual = datetime.now()
    dia = fecha_actual.day
    mes = fecha_actual.strftime("%B").upper()
    mensaje = f"Entrenamiento {dia_semana} {dia} de {mes} a las 21 horas."
    ubicacion = "FUERA" if dia_semana == "LUNES" else "PABELLÓN"
    opciones = ["Sí", "No", "Entrenador"]
    encuesta_texto = f"{mensaje} {ubicacion}\n\n{TXT}"
    
    poll_message = await context.bot.send_poll(chat_id=GROUP_CHAT_ID, question=encuesta_texto, options=opciones, is_anonymous=False)
    
    # Guardamos la relación entre encuesta y grupo
    context.bot_data[poll_message.poll.id] = GROUP_CHAT_ID

async def recibir_respuesta(update: Update, context: CallbackContext) -> None:
    global respuestas_si

    respuesta = update.poll_answer
    usuario_nombre = respuesta.user.first_name
    opcion_elegida = respuesta.option_ids[0] if respuesta.option_ids else None

    opciones = ["Sí", "No", "Entrenador"]

    if opcion_elegida is not None and 0 <= opcion_elegida < len(opciones):
        respuesta_texto = opciones[opcion_elegida]

        # Enviar las respuestas a tu chat privado
        await context.bot.send_message(chat_id=TU_CHAT_ID, text=f"{usuario_nombre} respondió: {respuesta_texto}")

        # Contar respuestas afirmativas ("Sí")
        if respuesta_texto == "Sí":
            respuestas_si += 1

async def enviar_resumen_entrenamiento(context: CallbackContext) -> None:
    global respuestas_si

    # Determinar si hay suficientes personas
    if respuestas_si >= 8:
        mensaje = "✅ Hay suficientes personas para entrenar hoy."
    else:
        mensaje = "❌ No hay suficientes personas para entrenar hoy."

    # Enviar mensaje privado al organizador
    await context.bot.send_message(chat_id=TU_CHAT_ID, text=mensaje)

    # Reiniciar el contador para el próximo día
    respuestas_si = 0

async def enviar_MON(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(context, "LUNES")

async def enviar_WEN(update: Update, context: CallbackContext) -> None:
    await enviar_encuesta_entrenamiento(context, "MIÉRCOLES")

def programar_encuestas(application: Application):
    job_queue = application.job_queue
    job_queue.run_daily(lambda context: context.job.application.create_task(enviar_encuesta_entrenamiento(context, "LUNES")),
                        time=time(8, 0, tzinfo=timezone.utc), days=(0,))  # Lunes

    job_queue.run_daily(lambda context: context.job.application.create_task(enviar_encuesta_entrenamiento(context, "MIÉRCOLES")),
                        time=time(8, 0, tzinfo=timezone.utc), days=(2,))  # Miércoles

async def start(update: Update, context: CallbackContext) -> None:
    global GROUP_CHAT_ID
    GROUP_CHAT_ID = update.message.chat_id  
    await update.message.reply_text(
        "🏀 Bot Iniciado. Estoy programado para enviar encuestas los Lunes y Miércoles a las 8 AM. Si por lo que sea no se envían usa /MON y /WEN 🏀 \n"
        "🏀 Las encuestas de los partidos se tienen que hacer de forma manual, para mandarlas por comandos, utiliza /JORN_['A' / 'B']_['nº de la Jornada'] 🏀 \n"
        "🏀 Esta versión del Bot (1.2.0) solo tiene hasta la Jornada nº 22, (no aparecen más en Swish), en cuanto se actualice la web, se añadirán más jornadas. 🏀 \n"
        "🏀 IMPORTANTE, MANDAD SOLO UN COMANDO/ENCUESTA PARA EVITAR CONFUSIONES. 🏀 \n"
        "Cualquier duda escribir por privado a @Arturitown, y si alguien quiere contribuir a mi desarrollo teneis el repositorio público de GitHub aquí : https://github.com/arturosasan/CBEV_Bot"

    )
	
# Función genérica para enviar encuestas de jornadas
async def enviar_JORNADA(update: Update, context: CallbackContext, equipo: str, jornada: int, fecha: str, rival: str, hora: str, encuentro: str) -> None:
    opciones = ["Sí", "No", "Disponible", "Entrenador"]
    encuesta_texto = f"Partido LIGA {fecha} vs {rival}, a las {hora}, {encuentro}"
    poll_message = await context.bot.send_poll(chat_id=GROUP_CHAT_ID, question=encuesta_texto, options=opciones, is_anonymous=False)
    context.bot_data[poll_message.poll.id] = poll_message.chat.id

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


def main() -> None:
    application = Application.builder().token(TOKEN).build()
    
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
    application.add_handler(PollAnswerHandler(recibir_respuesta))

    # Programar el resumen de respuestas a las 18:00
    application.job_queue.run_daily(enviar_resumen_entrenamiento, time=time(18, 0, tzinfo=timezone.utc))

    application.run_polling()

if __name__ == '__main__':
    main()
