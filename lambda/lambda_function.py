import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
from utils import Federal
import random

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class LaunchRequestHandler(AbstractRequestHandler):
    """A Skill foi iniciada"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá, o que você quer saber ? Diga último resultado, resultado do concurso 5000 ou peça um palpite."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('O que deseja saber ?', speak_output))
                .ask(speak_output)
                .response
        )

class RandomFederalIntentHandler(AbstractRequestHandler):
    """A Skill foi iniciada"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("RandomFederalIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Olá, o que você quer saber ? Diga último resultado, resultado do concurso 5000 ou peça um palpite."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('O que deseja saber ?', speak_output))
                .ask(speak_output)
                .response
        )

class LastFederalIntentHandler(AbstractRequestHandler):
    """Gera um número aleatório e fornece como palpite"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("LastFederalIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        federal = Federal()
        resultado = federal.get()
        concurso = str(resultado['numero'])
        speak_output = 'O resultado da Loteria Federal pelo concurso '+concurso[:2]+concurso[2:]+', no dia '+resultado['dataApuracao']+' foi: 1º Prêmio: '+resultado['listaDezenas'][0][2:4]+' '+resultado['listaDezenas'][0][4:]+', 2º Prêmio: '+resultado['listaDezenas'][1][2:4]+' '+resultado['listaDezenas'][1][4:]+', 3º Prêmio: '+resultado['listaDezenas'][2][2:4]+' '+resultado['listaDezenas'][2][4:]+', 4º Prêmio: '+resultado['listaDezenas'][3][2:4]+' '+resultado['listaDezenas'][3][4:]+', 5º Prêmio: '+resultado['listaDezenas'][4][2:4]+' '+resultado['listaDezenas'][4][4:]+'. Este resultado foi fornecido pela Caixa Econômica Federal.'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('Palpite Loteria Federal', speak_output))
                .response
        )

class NumberFederalIntentHandler(AbstractRequestHandler):
    """A Skill foi iniciada"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_intent_name("NumberFederalIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        concurso = int(handler_input.request_envelope.request.intent.slots["number"].value)
        federal = Federal()
        resultado = federal.get(concurso)
        concurso = str(resultado['numero'])
        speak_output = 'O resultado da Loteria Federal pelo concurso '+concurso[:2]+concurso[2:]+', no dia '+resultado['dataApuracao']+' foi: 1º Prêmio: '+resultado['listaDezenas'][0][2:4]+' '+resultado['listaDezenas'][0][4:]+', 2º Prêmio: '+resultado['listaDezenas'][1][2:4]+' '+resultado['listaDezenas'][1][4:]+', 3º Prêmio: '+resultado['listaDezenas'][2][2:4]+' '+resultado['listaDezenas'][2][4:]+', 4º Prêmio: '+resultado['listaDezenas'][3][2:4]+' '+resultado['listaDezenas'][3][4:]+', 5º Prêmio: '+resultado['listaDezenas'][4][2:4]+' '+resultado['listaDezenas'][4][4:]+'. Este resultado foi fornecido pela Caixa Econômica Federal.'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('O que deseja saber ?', speak_output))
                .ask(speak_output)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """O usuário pediu ajuda"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = 'Você pode dizer "último resultado" para ouvir o último resultado disponível, resultado do concurso mais o número do concurso que você quer, por exemplo, "resultado do concurso 5000" para ouvir o resultado do concurso 5000, "me dê um palpite" para ouvir um número gerado aleatoriamente.'

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('Você pode dizer:', "• \"Último resultado\" para ouvir o último resultado disponível. \n• Resultado do concurso + o número do concurso que você quer. Ex: \"Resultado do concurso 5000\", para ouvir o resultado do concurso 5000. \n• \"Me dê um palpite\" para ouvir um número gerado aleatoriamente."))
                .ask(speak_output)
                .response
        )

class CancelOrStopIntentHandler(AbstractRequestHandler):
    """O usuário encerrou a skill"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Tchau, espero você na próxima."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('Tchau!', speak_output))
                .response
        )

class FallbackIntentHandler(AbstractRequestHandler):
    """Não entendido o que o usuário disse"""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.FallbackIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        logger.info("In FallbackIntentHandler")
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
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response

class IntentReflectorHandler(AbstractRequestHandler):
    """Revela intents não definido"""

    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = 'Você está solicitando o intent '+intent_name+', mas ele ainda não está definido'

        return (
            handler_input.response_builder
            .speak(speak_output)
            # .ask("add a reprompt if you want to keep the session open for the user to respond")
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

        speak_output = "Desculpa, encontrei um erro. Tente novamente mais tarde."
        return (
            handler_input.response_builder
                .speak(speak_output)
                .set_card(SimpleCard('Erro meu :(', speak_output))
                .response
        )

sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(RandomFederalIntentHandler())
sb.add_request_handler(LastFederalIntentHandler())
sb.add_request_handler(NumberFederalIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(FallbackIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())

sb.add_request_handler(IntentReflectorHandler())
sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()