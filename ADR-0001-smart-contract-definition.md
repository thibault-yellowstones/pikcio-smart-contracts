# Définition d'un Smart Contract

On s'intéresse ici à la façon de permettre à un utilisateur de définir un
**Smart Contract Pikcio**. Cet article énonce les différentes options évaluées
ainsi que celles choisies. 

## Révision
- 1.0.0 : 22/06/2018

## Contexte
Pour rappel, on définit ici le **Smart Contract** comme un bloc de code
contenant des fonctions pouvant être invoquées par l'utilisateur après
soumission dudit contrat à la chaîne de blocs.

Le langage de définition est Python 2.7.

Pour définir un Smart Contract, il faut pouvoir identifier sans ambiguïté:
- **La portée du contrat dans le code**: Quelles sont le fonctions qui peuvent
être appelées et quelles sont celles qui sont seulement internes ?
- **Les types utilisés et utilisables**: Comment marquer le type d'un paramètre
dans un langage à typage dynamique ?
- **Les variables constantes, stockées**: Quelles sont les variables dont
l'état final doit être sauvé et restoré d'appel en appel ?

### Stratégie
Pour trancher parmi plusieurs options, on choisit de privilégier les choix qui 
n'impliquent pas de développement supplémentaire. Publier une API permettrait 
plus de liberté et de créativité mais nécessite un investissement
supplémentaire et ralentit les évolutions (processus de release, 
rétro-compatibilité...).

Pour orienter les choix, on pourra faire la comparaison avec
d'autres crypto-monnaies.

## La portée du contrat
Dans cette section on cherche à répondre aux questions:
1. Quelle partie du fichier/bloc de code soumis fait partie du contrat ?
2. A l'intérieur du contrat, quels sont les points d'entrées ?

### Délimitation du contrat

#### Options

2 options ici:
- Le contrat est le fichier/bloc de code soumis tout entier.
- Le contrat est une structure (classe, fonction) au sein du bloc.

La première option est moins contraignante puisqu'elle élimine le problème de 
distinction du contrat du reste du code. En revanche elle implique qu'il n'y a
qu'un seul contrat par fichier (pas de soumission multiple) et elle mets plus
de poids sur la question de distinction des points d'entrée et des variables
constantes.

La deuxième option est plus flexible car elle permet de différencier ce qui
fait partie du contrat (points d'entrées, variables constantes) de ce qui ne
l'est pas. En revanche elle nécessite une convention pour identifier qu'un bloc
de code est un contrat.

*NEO* et *Ethereum* ont tous les deux optés pour la deuxième option. Le choix
était forcé pour *NEO* étant donné que le langage *C#* est purement objet mais 
*Ethereum* l'a fait par design avec *Solidity*.

#### Analyse

Si la deuxième option est plus flexible, elle n'est pas forcément nécessaire
dans un premier temps. Favoriser la simplicité semble prioritaire. De plus, la
deuxième option implique de structurer la définition d'un contrat, par exemple:

```python
def contract_test():

    data = 3

    def endpoint():
        global data
        data += 3
        return data
```
ou bien :
```python
class contract_test(object):
    data = 3

    @staticmethod
    def endpoint():
        contract_test.data += 3
        return data
```

Le premier exemple (fonctions imbriquées) n'est pas facilement accessible par
introspection, ce qui implique que l'extraction des points d'entrées et des
variables constantes sera plus complexe.

Le deuxième exemple fonctionne mieux mais il pose beaucoup de questions:
- Faut-il autoriser les méthodes d'objet (**self**) ? Les méthodes de classe
(**cls**) ?
- Droit à un constructeur ?
- Quid de l'héritage ?

Cette solution pose plus de questions qu'elle n'en résout.

### Distinction des points d'entrée

#### Options

- Conventions de nommage
- Configuration active

##### Convention

Utiliser une convention est peu verbeux et assez répandu en Python (`self`,
`cls` ne sont pas des mots réservés).

On pourrait par exemple se reposer sur celle qui consiste à préfixer
d'un `_` toute fonction d'un module (ou membre d'une classe) qui n'a pas
vocation à être publique. Ainsi, seules les fonctions "publiques" du module
seront considérées comme des points d'entrée:

```python
# Fonction interne
def _do_internal_query():
	pass
	
# Point d'entrée
def my_endpoint():
	pass
```

##### Configuration

La méthode la plus concise et élégante serait probablement d'utiliser un 
**décorateur**, par exemple:
```python
def do_internal_query():
	pass

@pkc_smart_contract_endpoint
def my_endpoint():
	pass
```
Une autre technique consiste à forcer l'utilisateur à ajouter un champ de
métadonnées dans son module avec un format prédéfini:
```python
def do_internal_query():
	pass

def my_endpoint():
	pass

__PKC_CONTRACT_META = {
	"endpoints": [
		"my_endpoint"
	]
}
```

#### Analyse

La convention de nommage `_` est simple, lisible et facile à mettre en place.
Plusieurs IDE (dont PyCharm) utilisent déjà cette convention pour guider leur 
autocompletion. Son inconvénient est qu'étant peu précise, il est
éventuellement possible qu'elle finisse par être gênante.

Le décorateur est intéressant mais nécessite de publier une API, ce qu'on évite
à ce stade.

Le champ de métadonnées est plus verbeux mais aussi plus flexible:
- En plus des points d'entrée, on pourrait y indiquer les
**variables constantes** et autres métadonnées (version, auteur...)
- Il n'y a pas besoin de changer le code source pour changer le contenu du
contrat.

Son principal désavantage est qu'il doit être généré et maintenu par le
développeur.

### Types utilisés et utilisables

On ne peut pas publier l'ABI d'un Smart Contract sans connaître la signature 
typée de ses fonctions. 
Python 3 permet d'annoter les fonctions pour leur ajouter un type. Cela n'est
pas possible avec Python 2.7.

Le problème a déjà été étudié par la communauté et la solution la plus simple 
est de fournir les types en commentaire de la fonction (commentaires qui 
peuvent être introspectés).

#### mypy
mypy est un projet open source visant a effectuer un *type checking* des appels
de fonction réalisés au sein d'un programme. Le programme se sert des
annotations en Python 3 et d'une convention d'écriture des types en commentaires
pour Python 2.

Le projet est activement maintenu et parait.


 **Dans un premier
temps, il parait plus facile d'assumer qu'un module python est un contrat.** Il
sera toujours possible d'enrichir la structure par la suite.
