<?php
namespace NethServer\Module\Dashboard\Applications;

/**
 * Transmission web interface
 *
 * @author stephane de labrusse
 */
class Transmission extends \Nethgui\Module\AbstractModule implements \NethServer\Module\Dashboard\Interfaces\ApplicationInterface
{

    public function getName()
    {
        return "Transmission";
    }

    public function getInfo()
    {
         $webapp = $this->getPlatform()->getDatabase('configuration')->getProp('transmission-daemon','Name');
         $webfolder = $this->getPlatform()->getDatabase('configuration')->getProp('transmission','WebNameDir');
         $host = explode(':',$_SERVER['HTTP_HOST']);
         return array(
            'url_Daemon' => "https://".$host[0]."/$webapp",
            'url_WebFolder' => "https://".$host[0]."/$webfolder"
         );
    }
}
