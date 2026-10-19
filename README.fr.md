# Liquidité oisive et ciblage de l'investissement

**Projet de fin d'année · Analyse bancaire · Python · Aide à la décision**

**Auteur :** [Hamza Zhiri](https://github.com/zhiriii03) · INSEA

[English version](README.md) · [Méthodologie](METHODOLOGY.md) · [Périmètre publié](PUBLICATION_SCOPE.md)

## Problématique

Quels clients combinent une capacité financière potentiellement mobilisable et
un profil favorable à une démarche de placement ? Dans quelles conditions une
migration de leurs dépôts serait-elle intéressante pour la banque distributrice ?

Ce PFA relie la préparation des données, la segmentation, la modélisation de la
propension, le ciblage et l'analyse financière. L'objectif est d'éclairer une
décision commerciale et ses conséquences économiques.

## Démarche

1. **Fiabiliser les données** : déduplication au grain client, contrôle des incohérences,
   diagnostic des valeurs manquantes et vérification des inclusions entre poches de dépôt.
2. **Distinguer les usages de compte** : banque principale, compte de transit présumé
   et compte inactif, avec les limites de cette interprétation.
3. **Comparer les modèles** : régression logistique, forêt aléatoire et gradient boosting
   sur histogrammes, avec validation croisée stratifiée à cinq plis.
4. **Prioriser les prospects** : croiser les rangs percentiles de capacité et de propension
   au sein de chaque segment.
5. **Simuler des montants** : produire des scénarios conditionnels de migration.
6. **Examiner l'économie de la campagne** : commissions, coûts de contact, marge de dépôt
   abandonnée et devenir des fonds sans sollicitation.

Le projet conserve l'interprétation du score de classification de statut comme
une propension commerciale. Cette utilisation repose sur une hypothèse de transfert
qui doit ensuite être vérifiée sur les conversions d'une campagne pilote.

## Contenu de cette édition publique

Cette version présente la méthode et une **démonstration pédagogique entièrement
synthétique**. Elle ne contient ni données bancaires, ni dossiers clients, ni résultats
internes, ni modèle ajusté, ni rapport intégral du stage.

Le script public est une reconstruction simplifiée créée pour cette publication.
Ses clients, montants, paramètres et scores sont fictifs. Les scores sont des entrées
générées, pas les sorties d'un modèle entraîné. Les résultats de la démonstration
ne sont donc pas ceux du PFA original.

## Exécution

Python **3.10 ou plus récent**, sans dépendance supplémentaire :

```bash
python demo.py
python -m unittest -v
```

Le script affiche un classement de prospects fictifs, des quantiles simulés et un
scénario économique. Il n'effectue aucun appel réseau et n'écrit aucun fichier.

## Apport du projet

La capacité indique un volume potentiel ; la propension sert au classement.
L'analyse financière vérifie ensuite si ce volume peut créer de la valeur.
Un bon classement statistique et un ROI positif sur les seules commissions ne
suffisent pas, à eux seuls, à établir la rentabilité globale d'une campagne.

Le travail original est documenté avec Python, pandas, NumPy, scikit-learn,
des mesures DAX et un rapport LaTeX. Le script public n'implémente que les
mécanismes pédagogiques de ciblage et de simulation.

Il s'agit d'un travail académique personnel, sans approbation institutionnelle
implicite ni recommandation de placement individuelle.
