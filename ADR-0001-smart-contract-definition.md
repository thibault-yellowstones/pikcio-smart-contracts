# Définition d'un Smart Contract

On s'intéresse ici à la façon de permettre à un utilisateur de définir un
**Smart Contract Pikcio**. Cet article énonce les différentes options évaluées
ainsi que celles choisies. 

## Révision
- 1.0.0 : 22/06/2018

## Contexte
Pour rappel, on définit ici le **Smart Contract** comme un bloc de code
contenant des fonctions pouvant être invoquées par l'utilisateur après soumission
dudit contrat à la chaîne de blocs.

Pour définir un Smart Contract, il faut pouvoir identifier sans ambiguïté:
- **La portée du contrat dans le code**: Quelles sont le fonctions qui peuvent être appelées
et quelles sont celles qui sont purement utilitaires ?
- **Les types utilisés et utilisables**: Comment marquer le type d'un paramètre dans un langage à typage dynamique ?
- **Les variables constantes, stockées**: Quelles sont les variables dont l'état final doit être sauvé d'appel en appel ?

### Stratégie
Pour trancher parmi plusieurs options, on choisit de privilégier les choix qui n'impliquent pas de développement supplémentaire.
En effet la création d'un package Python nécessite un investissement en temps non négligeable et ralentit les évolutions.

On pourra faire la comparaison avec d'autres crypto-monnaies.

## La portée du contrat

1. Quelle partie du fichier/bloc de code soumis fait partie du contrat ?
2. A l'intérieur du contrat, quels sont les points d'entrées ?

### Délimitation du contrat

#### Options

2 options ici:
- Le contrat est le fichier/bloc de code soumis tout entier.
- Le contrat est une structure (classe, fonction) au sein du bloc.

La première option est moins contraignante puisqu'elle élimine le problème de 
distinction du contrat du reste du code. En revanche elle implique qu'il n'y a
qu'un seul contrat par fichier (pas de soumission multiple).

La deuxième option est plus flexible car elle permet de différencier ce qui
fait partie du contrat (points d'entrées, variables constantes) de ce qui ne
l'est pas. En revanche elle nécessite une convention pour identifier qu'un bloc
est un contrat.

NEO et Ethereum ont tous les deux optés pour la deuxième option. Le choix était 
forcé pour NEO étant donné que le langage *C#* est purement objet mais Ethereum
avait son libre arbitre aec *Solidity*.

#### Choix

Si la deuxième option est plus flexible, elle n'est pas forcément nécessaire
dans un premier temps. Favoriser la simplicité est plus important. De plus, la
deuxième option implique de structurer les contrats, par exemple:
```python
def contract_test():

    data = 3

    def endpoint():
        global data
        data += 3
        return data
```
ou bien
```python
class contract_test(object):
    data = 3

    @staticmethod
    def endpoint():
        contract_test2.self.data += 3
        return data
```

Le premier exemple (fonctions imbriquées) n'est pas facilement accessible par
introspection, ce qui implique que l'extraction des points d'entrées et des
variables constantes sera plus complexe.

Le deuxième exemple fonctionne mieux mais il pose beaucoup de questions:
- Faut-il autoriser les méthodes d'objet (**self**) ? Les méthodes de classe (**cls**) ?
- Droit à un constructeur ?
- Quid de l'héritage ?

**Dans un premier temps il semble plus facile d'assumer qu'un module python est un contrat**

### Distinction des points d'entrées

Si l'on avait