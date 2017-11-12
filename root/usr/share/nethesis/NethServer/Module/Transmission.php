<?php
namespace NethServer\Module;


use Nethgui\System\PlatformInterface as Validate;

/**
 * Control transmission access to the system
 * 
 * @author stephane de Labrusse <stephdl@de-labrusse.fr>
 */
class Transmission extends \Nethgui\Controller\AbstractController
{

    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $base)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($base, 'Configuration', 6);
    }

    public function initialize()
    {
        parent::initialize();
        $this->declareParameter('status', Validate::SERVICESTATUS, array('configuration', 'transmission', 'status'));
        $this->declareParameter('Users', Validate::ANYTHING, array('configuration', 'transmission', 'Users'));
        $this->declareParameter('Webaccess', $this->createValidator()->memberOf('private','public'), array('configuration', 'transmission', 'Webaccess'));
    }

    public static function splitLines($text)
    {
        return array_filter(preg_split("/[,;\s]+/", $text));
    }
    public function readUsers($dbList)
    {
        return implode("\r\n", explode(',' ,$dbList));
    }
    public function writeUsers($viewText)
    {
        return array(implode(',', self::splitLines($viewText)));
    }

    public function validate(\Nethgui\Controller\ValidationReportInterface $report)
    {
        parent::validate($report);
        $itemValidator = $this->getPlatform()->createValidator(\Nethgui\System\PlatformInterface::USERNAME);
        foreach (self::splitLines($this->parameters['Users']) as $v) {
            if ( ! $itemValidator->evaluate($v)) {
                $report->addValidationErrorMessage($this, 'Users', 'Must be a user name', array($v));
                break;
            }
        }
    }

    protected function onParametersSaved($changedParameters)
    {
        parent::onParametersSaved($changedParameters);
        $this->getPlatform()->signalEvent('nethserver-transmission-save');
    }

}
