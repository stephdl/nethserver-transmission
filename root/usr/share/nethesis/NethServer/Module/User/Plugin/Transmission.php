<?php
namespace NethServer\Module\User\Plugin;
use Nethgui\System\PlatformInterface as Validate;
use Nethgui\Controller\Table\Modify as Table;
/**
 * Transmission user plugin
 * 
 * @author Stephane de Labrusse <stephdl@de-labrusse.fr> 
 */
class Transmission extends \Nethgui\Controller\Table\RowPluginAction
{
    protected function initializeAttributes(\Nethgui\Module\ModuleAttributesInterface $base)
    {
        return \Nethgui\Module\SimpleModuleAttributesProvider::extendModuleAttributes($base, 'Service', 10);
    }
    public function initialize()
    {
        $this->setSchemaAddition(array(
            array('TransmissionWebUI', Validate::SERVICESTATUS , Table::FIELD),
            array('TransmissionWebFolder', Validate::SERVICESTATUS , Table::FIELD),
            array('TransmissionSmbFolder', Validate::SERVICESTATUS , Table::FIELD),

        ));
        $this->setDefaultValue('TransmissionWebUI', 'disabled');
        $this->setDefaultValue('TransmissionWebFolder', 'disabled');
        $this->setDefaultValue('TransmissionSmbFolder', 'disabled');

        parent::initialize();
    }
}
