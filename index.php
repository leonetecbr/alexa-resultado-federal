<?php
date_default_timezone_set('America/Bahia');

require __DIR__.'/vendor/awsmug/alexa-php-sdk/src/alexa-sdk.php';
require __DIR__.'/vendor/autoload.php';

use Dotenv\Dotenv;
use Alexa\Exception;
use Leone\Loteria\Federal\Skill;

$dotenv = Dotenv::createImmutable(__DIR__);
$dotenv->load();

$skill = new Skill($_ENV['AMAZON_SKILL_ID']);

try{
	$skill->run();
} catch(Exception $e) {
	$skill->log($e->getMessage());
	echo $e->getMessage();
}