<?php
namespace Results\Controller;

use \Alexa\Skill_Template;
use \Results\Api;

class AllSkill extends Skill_Template {
  
  /**
   * Pega o texto para envio do resultado e transforma no JSON  
   */
  private function sendResultFederal(){
    $intent_text = Api\Federal::getText();
	  $intent_card = Api\Federal::getCard();
		$this->output()->response()->output_speech()->set_text($intent_text);
		$this->output()->response()->card()->set_title('Resultado da Loteria Federal');
		$this->output()->response()->card()->set_text($intent_card);
  }
  
  /**
   * Pega o texto para emvio do próximo sorteio e transforma no JSON  
   */
  private function sendNextFederal(){
    $intent_text = Api\Federal::getNext();
		$this->output()->response()->output_speech()->set_text($intent_text);
		$this->output()->response()->card()->set_title('Próximo sorteio da Loteria Federal');
		$this->output()->response()->card()->set_text($intent_text);
		
		$this->output()->response()->end_session();
  }
  
  /**
   * Processa o Intent e direciona ao método correspondente
   */
  private function processIntent(){
    switch ($this->input()->request()->intent()->get_name()) {
      case 'AMAZON.StopIntent':
        $this->end_request();
        break;
      
      case 'ExitIntent':
        $this->end_request();
        break;
      
      case 'NextFederalIntent':
        $this->sendNextFederal();
        break;
        
      case 'RepeatFederalIntent':
        $this->sendResultFederal();
        break;
      
      default:
        $this->failed_request();
    }
  }
  
  /**
   * Um Intent foi recebibo
   */
	public function intent_request() {
	  $this->processIntent();
	}
	
	/**
   * A Skill foi iniciada
   */
	public function launch_request() {
  	$this->sendResultFederal();
	}
	
	/**
   * Intent não locaizado
   */
	public function failed_request(){
	  $this->output()->response()->output_speech()->set_text('Não entendi o que você disse, tente novamente de outra forma.');
		$this->output()->response()->card()->set_title('Não entendi!');
		$this->output()->response()->card()->set_text('Não entendi o que você disse, tente novamente de outra forma.');

		$this->output()->response()->end_session();
	}
	
	/**
   * A Skill foi encerrada
   */
	public function end_request() {
  	$this->output()->response()->output_speech()->set_text('Tchau, espero você na próxima!');
		$this->output()->response()->card()->set_title('Tchau!');
		$this->output()->response()->card()->set_text('Tchau, espero você na próxima!');

		$this->output()->response()->end_session();
	}
}