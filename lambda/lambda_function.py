import logging
import random
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from utils import Federal, getText, getCard, getDezenas

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """A Skill foi iniciada"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type('LaunchRequest')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Olá, o que você quer saber ? Diga último resultado, últimas dezenas, resultado do concurso 5000 ou peça um palpite. '

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('O que deseja saber ?', speak_output))
            .ask(speak_output)
            .response
        )


class RandomFederalIntentHandler(AbstractRequestHandler):
    """O usuário pediu palpite"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('RandomFederalIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        palpite = random.randint(0, 9999)
        palpite = str(palpite).zfill(4)
        palpite = palpite[:2]+' '+palpite[2:]
        speak_output = 'Pensei! Mas antes de falar, quero te dizer que ele é apenas um número gerado aleatoriamente, não garanto que ele seja sorteado. Ok? Eu pensei no número '+palpite

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Palpite da Loteria Federal', speak_output))
            .set_should_end_session(True)
            .response
        )


class LastFederalIntentHandler(AbstractRequestHandler):
    """O usuário pediu último resultado"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('LastFederalIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        federal = Federal()
        resultado = federal.get()
        if 'erro' in resultado:
            print(resultado)
            speak_output = 'Estamos com problemas para obter o resultado! Aguarde alguns minutos antes de tentar novamente.'
            card = speak_output
            return (
                handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('Resultado da Loteria Federal', card))
                .set_should_end_session(True)
                .response
            )

        speak_output = getText(resultado)+' Quer que eu repita ?'
        card = getCard(resultado)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Resultado da Loteria Federal', card))
            .ask('Quer que eu repita ?')
            .response
        )


class LastDezenaIntentHandler(AbstractRequestHandler):
    """O usuário pediu último resultado apenas com as dezenas"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('LastDezenaIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        federal = Federal()
        resultado = federal.get()
        if 'erro' in resultado:
            print(resultado)
            speak_output = 'Estamos com problemas para obter o resultado! Aguarde alguns minutos antes de tentar novamente.'
            card = speak_output
        else:
            speak_output = getDezenas(resultado)
            card = getCard(resultado)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Resultado da Loteria Federal', card))
            .set_should_end_session(True)
            .response
        )


class NumberFederalIntentHandler(AbstractRequestHandler):
    """Usuário pediu o resultado de um concurso específico"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('NumberFederalIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        concurso = handler_input.request_envelope.request.intent.slots['number'].value
        concurso = 0 if not concurso.isdigit() else int(concurso)

        federal = Federal()
        resultado = federal.get(concurso)
        if 'erro' in resultado:
            print(resultado)
            concurso = str(concurso)
            if len(str(concurso)) == 4:
                concurso = concurso[:2]+' '+concurso[2:]
            speak_output = f'Não foi possível obter o resultado do concuso {concurso}. Quer ouvir o último resultado ?'
            card = resultado['mensagem']
        else:
            speak_output = getText(resultado) + \
                ' Quer ouvir o último resultado ?'
            card = getCard(resultado)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Resultado da Loteria Federal', card))
            .ask('Quer ouvir o último resultado ?')
            .response
        )


class NumberDezenaIntentHandler(AbstractRequestHandler):
    """Usuário pediu as dezenas de um concurso específico"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name('NumberDezenaIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        concurso = handler_input.request_envelope.request.intent.slots['number'].value
        concurso = 0 if not concurso.isdigit() else int(concurso)

        federal = Federal()
        resultado = federal.get(concurso)
        try:
            speak_output = resultado['mensagem']
            card = resultado['mensagem']
        except KeyError:
            speak_output = getDezenas(resultado)
            card = getCard(resultado)

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Resultado da Loteria Federal', card))
            .set_should_end_session(True)
            .response
        )


class HelpIntentHandler(AbstractRequestHandler):
    """O usuário pediu ajuda"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('AMAZON.HelpIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Você pode dizer "último resultado" para ouvir o último resultado disponível, "últimas dezenas" para ouvir apenas as dezenas do último resultado disponível, resultado do concurso mais o número do concurso que você quer, por exemplo, "resultado do concurso 5000" para ouvir o resultado do concurso 5000, dezenas do concurso mais o número do concurso que você quer, por exemplo, "dezenas do concurso 5000" para ouvir apenas as dezenas do resultado do concurso 5000, "me dê um palpite" para ouvir um número gerado aleatoriamente.'

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Você pode dizer:', "• \"Último resultado\" para ouvir o último resultado disponível.\n • \"Últimas dezenas\" para ouvir apenas as dezenas do último resultado disponível.\n• Resultado do concurso + o número do concurso que você quer. Ex: \"Resultado do concurso 5000\", para ouvir o resultado do concurso 5000.\n• Dezenas do concurso + o número do concurso que você quer. Ex: \"Dezenas do concurso 5000\", para ouvir apenas as dezenas do resultado do concurso 5000. \n• \"Me dê um palpite\" para ouvir um número gerado aleatoriamente."))
            .ask(speak_output)
            .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """O usuário encerrou a skill"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name('AMAZON.CancelIntent')(handler_input) or
                ask_utils.is_intent_name('AMAZON.StopIntent')(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Tchau, espero você na próxima.'

        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Tchau!', speak_output))
            .set_should_end_session(True)
            .response
        )


class FallbackIntentHandler(AbstractRequestHandler):
    """Não entendido o que o usuário disse"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name('AMAZON.FallbackIntent')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info('In FallbackIntentHandler')
        speech = 'Não entendi o que você disse, tente novamente de outra forma. Caso não saiba o que falar diga "ajuda" e eu vou te ajudar.'

        return (
            handler_input.response_builder
            .speak(speech)
            .set_card(SimpleCard('Não entendi!', speech))
            .ask(speech)
            .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Sessão finalizada"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type('SessionEndedRequest')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """Revela intents não definido"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type('IntentRequest')(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = 'Você está solicitando o intent ' + \
            intent_name+', mas ele ainda não está definido'

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask('add a reprompt if you want to keep the session open for the user to respond')
            .set_should_end_session(True)
            .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Erro no código"""

    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = 'Desculpa, encontrei um erro. Tente novamente mais tarde.'
        return (
            handler_input.response_builder
            .speak(speak_output)
            .set_card(SimpleCard('Erro meu :(', speak_output))
            .set_should_end_session(True)
            .response
        )


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RandomFederalIntentHandler())
sb.add_request_handler(LastFederalIntentHandler())
sb.add_request_handler(LastDezenaIntentHandler())
sb.add_request_handler(NumberFederalIntentHandler())
sb.add_request_handler(NumberDezenaIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
