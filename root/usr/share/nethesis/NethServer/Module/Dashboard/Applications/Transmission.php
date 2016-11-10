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
        return "Transmission Torrent";
    }

    public function getInfo()
    {
         $webapp = $this->getPlatform()->getDatabase('configuration')->getProp('transmission-daemon','Name');
         $host = explode(':',$_SERVER['HTTP_HOST']);
         return array(
            'url' => "https://".$host[0]."/$webapp",
         );
    }
}
