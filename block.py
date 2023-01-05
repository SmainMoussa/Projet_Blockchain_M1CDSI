# MOUSSA SMAIN - POIGNARD KEVIN - VANDENBOREN SIMON  M1 CDSI


# json est un format d'échange de données léger inspiré de la syntaxe littérale d'objet JavaScript, il va nous permettre ici d'enregistrer
# nos données dans la blockchain
import json

# Flask est utilisé pour développer des applications Web en python, implémentées sur Werkzeug et Jinja2. Les avantages de l'utilisation du 
# framework Flask sont les suivants : Un serveur de développement intégré et un débogueur rapide sont fournis.
# On va ici utiliser "app" et "jsonify" pour pouvoir afficher la blockchain
from flask import Flask, jsonify

# Le module datetime fournit des classes pour manipuler les dates et les heures.
import datetime

# Ce module implémente une interface commune à de nombreux algorithmes de hachage et de résumé de message sécurisés.
# Sont inclus les algorithmes de hachage sécurisés FIPS SHA1, SHA224, SHA256, SHA384 et SHA512 (définis dans FIPS 180-2)
# ainsi que l'algorithme MD5 de RSA (défini dans Internet RFC 1321). Les termes « hachage sécurisé » et « résumé de message » 
# sont interchangeables. Les algorithmes plus anciens étaient appelés résumés de messages. Le terme moderne est hachage sécurisé.
import hashlib


# On définit la classe Blockchain
class Blockchain:
    # On va créer ici notre premier block avec un hash de "0" comme il sera le premier de la chaîne
	def __init__(init_de_fonction):
		init_de_fonction.chaine = [] # on initialise la chaine
		# apres initialisation, on le set à preuve = 1 et hash = 0 comme s'est le premier et c'est nous meme qui le créons
		init_de_fonction.creation_du_block(preuve=1, hash_precedent='0')
	# Après le premier block créé, on va pouvoir en créer d'autre à la suite gràce à cette fonction
	# on a besoin du hash du block precedent et la preuve pour vérifier si le hash miné correspond à la preuve
	def creation_du_block(init_de_fonction, preuve, hash_precedent):
		block = {'id_block': len(init_de_fonction.chaine) + 1,
				'temps': str(datetime.datetime.now()),
				'preuve': preuve,
				'hash_precedent': hash_precedent}
		init_de_fonction.chaine.append(block) # on ajoute le bloc
		return block

	# On affiche le bloc précèdent gràce à cette fonction
	def afficher_block_precedent(init_de_fonction):
		return init_de_fonction.chaine[-1] # il suffit de retourner le bloc d'avant

	# Ici, on a le preuve of work qui va définir si le block suivant miné à bien trouvé le hash du block précédent
	def proof_of_work(init_de_fonction, preuve_precedente):
		preuve_n = 1
		verification_de_preuve = False
		while verification_de_preuve is False:
			calcul_de_hash = hashlib.sha256( # calcul du hash
				str(preuve_n**2 - preuve_precedente**2).encode()).hexdigest()
			if calcul_de_hash[:5] == '00000': # s'il correspond à la clé de hashage, on valide
				verification_de_preuve = True
			else:
				preuve_n += 1
		return preuve_n

	def hash(init_de_fonction, block):
		bloc_coder = json.dumps(block, sort_keys=True).encode()
		return hashlib.sha256(bloc_coder).hexdigest()

	def validation_de_chaine(init_de_fonction, chaine):
		block_precedent = chaine[0] ## on vérifie si la chaine et valide avec la taille et le hash precedent
		id_block = 1
		while id_block < len(chaine):
			block = chaine[id_block]
			if block['hash_precedent'] != init_de_fonction.hash(block_precedent):
				return False
			preuve_precedente = block_precedent['preuve']
			preuve = block['preuve']
			calcul_de_hash = hashlib.sha256(
				str(preuve**2 - preuve_precedente**2).encode()).hexdigest()
			if calcul_de_hash[:5] != '00000':
				return False
			block_precedent = block
			id_block += 1
		return True

# On va tester dans une page web donc on utilise le module Flask identique à d'autre module tell que server.http de python...
app = Flask(__name__)
# Donc ici, on lance la fonction Blockchain()
blockchain = Blockchain()
# Ensuite le block sera miné

# on utilise la méthode get pour recupéré les données du minage 
@app.route('/mine_block', methods=['GET'])
def mine_block():
	block_precedent = blockchain.afficher_block_precedent()
	preuve_precedente = block_precedent['preuve']
	preuve = blockchain.proof_of_work(preuve_precedente)
	hash_precedent = blockchain.hash(block_precedent)
	block = blockchain.creation_du_block(preuve, hash_precedent)
	response = {'message': 'Nouveau bloc miné',
				'id_block': block['id_block'],
				'temps': block['temps'],
				'preuve': block['preuve'],
				'hash_precedent': block['hash_precedent']}
	return jsonify(response), 200

# On affiche les résultats du minage au format JSON gràce au module importé

# On affiche la chaine de blocs minés avec leurs informations 
@app.route('/get_chain', methods=['GET'])
def afficher_la_chaine():
	response = {'chaine': blockchain.chaine,
				'taille': len(blockchain.chaine)}
	return jsonify(response), 200

# On vérifie s'il le bloc est bien valid ou non

# On affiche si la chaine est valid ou non, si oui la blockchain est bien formée !
@app.route('/valid', methods=['GET'])
def est_ce_valide():
	valid = blockchain.validation_de_chaine(blockchain.chaine)
	if valid:
		response = {'message': 'La Blockchain est valide !'}
	else:
		response = {'message': 'La Blockchain n"est pas valide !'}
	return jsonify(response), 200

# Ligne de commande pour lancer le serveur en local sur le port 6892
app.run(host ='127.0.0.1', port = 6892)