<?php

/* @var $view Nethgui\Renderer\Xhtml */

echo $view->header()->setAttribute('template', $T('Transmission_header'));

echo $view->panel()

    ->insert($view->fieldsetSwitch('status', 'enabled',$view::FIELDSETSWITCH_CHECKBOX | $view::FIELDSETSWITCH_EXPANDABLE)->setAttribute('uncheckedValue', 'disabled')

->insert($view->radioButton('Webaccess', 'private'))
->insert($view->radioButton('Webaccess', 'public'))

->insert($view->textArea('Users', $view::LABEL_ABOVE)->setAttribute('dimensions', '5x30')->setAttribute('placeholder', $view['Users_default']))

);

echo $view->buttonList($view::BUTTON_SUBMIT | $view::BUTTON_HELP);
