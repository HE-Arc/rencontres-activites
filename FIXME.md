# Le fix me

## Installation

- pas de procédure d'installation (gdal etc.)
- version obsolète de Django
- un settings.py qui n'est pas prêt pour être déployé
- secret.py manquant et/ou pas documenté
- les warnings données par manage.py (timezone.now)
- migrations ne pouvant être lancées car le code fait du SQL au import
- un module "vendor"é sans aucune bonne raison
- des dépendences superflues non utilisée == mémoire gaspillée (e.g. simplejson)

## HTML

- script au début du `<body>`!?
- des 404.

## UX

- djanog-bootstrap4 ne gère pas aussi bien les erreurs que crispy forms
- vous mériteriez d'utiliser un ou deux boutons dits de _call-to-action_
- conseil général faites de petits formulaire en ne demandant que le strict nécessaire
- less is more
- en pratique les tags s'ajoutent de manière libre, un select bof bof.
- l'invariance d'une activité n'est pas vérifiée (e.g. min < max)
