<?php
namespace NethServer\Module\Dashboard\Applications;

/**
 * Transmission web interface
 *
 * @author stephane de labrusse
 */
class TransmissionWDL extends \Nethgui\Module\AbstractModule implements \NethServer\Module\Dashboard\Interfaces\ApplicationInterface
{

    public function getName()
    {
        return "Transmission Download";
    }

    public function getInfo()
    {
         $webfolder = $this->getPlatform()->getDatabase('configuration')->getProp('transmission','WebNameDir');
         $host = explode(':',$_SERVER['HTTP_HOST']);
         return array(
            'url' => "https://".$host[0]."/$webfolder"
         );
    }
}
