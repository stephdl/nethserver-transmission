<?php
echo $view->fieldset()->setAttribute('template', $T('TransmissionPermissionAccess_label'))
->insert($view->checkBox('TransmissionSmbFolder','enabled')->setAttribute('uncheckedValue', 'disabled'))
->insert($view->checkBox('TransmissionWebFolder','enabled')->setAttribute('uncheckedValue', 'disabled'))
->insert($view->checkBox('TransmissionWebUI','enabled')->setAttribute('uncheckedValue', 'disabled'));
