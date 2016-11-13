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

    protected function onParametersSaved($changedParameters)
    {
        parent::onParametersSaved($changedParameters);
        $this->getPlatform()->signalEvent('nethserver-transmission-save');
    }

}
