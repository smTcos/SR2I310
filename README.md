# Détection d'URLs Malveillantes avec LSTM

## Présentation du projet
Ce projet vise à **détecter des URLs malveillantes** à l’aide d’un **modèle LSTM** entraîné sur le dataset de base provenant de Kaggle :  
 **[Malicious URLs Dataset (600k URLs)](https://www.kaggle.com/datasets/sid321axn/malicious-urls-dataset)**  

Ce dataset classe les URLs en **4 catégories** :
-  **Benign** : Sites légitimes sans menace.
-  **Malware** : Héberge ou distribue des logiciels malveillants.
-  **Phishing** : Tentatives de vol d’informations via de fausses interfaces.
-  **Defacement** : Sites modifiés à des fins de vandalisme.

---

##  Organisation du projet
Le projet contient **trois expérimentations principales**, chacune avec son propre modèle :

 **`ESSAI1/`** →  **Features de base & Labels de base**  
 **`ESSAI2/`** →  **Features améliorés & Labels de base**  
 **`ESSAI3/`** →  **Features de base & Labels améliorés (ajout de `XSS` et `Path Traversal`)**

Chaque dossier contient :
- **Le modèle entraîné (`.h5`)**
- **Le tokenizer (`.pkl`)**
- **L’encodeur de labels (`.pkl`)**
- **Le dataset utilisé pour l’entraînement (`.csv`)**
- **Les résultats d'évaluation du modèle** (courbes de perte & accuracy)

---

## **Pourquoi utiliser un modèle LSTM ?**
Un LSTM (**Long Short-Term Memory**) est un type de réseau de neurones récurrent (**RNN**) capable de capturer **les relations séquentielles** dans les données.  
 **Les URLs ont une structure qui peut être analysée séquentiellement** → `https://www.bank-login.com` contient des indices de phishing que le LSTM peut apprendre.

### **Architecture du modèle**
Le modèle se compose de deux entrées :
1. **Une séquence tokenisée de l'URL** (traitée par un **LSTM**).
2. **Un vecteur de caractéristiques supplémentaires** (**longueur de l'URL, nombre de chiffres, présence de https, etc.**).

```python
# Entrée URL (tokenisée et padée)
url_input = Input(shape=(100,), name="url_input")
embedding = Embedding(input_dim=256, output_dim=64)(url_input)
lstm_out = LSTM(64, return_sequences=False)(embedding)

# Entrée des caractéristiques supplémentaires
features_input = Input(shape=(8,), name="extra_features")
dense_features = Dense(32, activation="relu")(features_input)

# Fusion des deux entrées
merged = Concatenate()([lstm_out, dense_features])
dense1 = Dense(64, activation="relu")(merged)
dropout = Dropout(0.5)(dense1)
output = Dense(4, activation="softmax", name="output")(dropout)

# Compilation du modèle
model_base = Model(inputs=[url_input, features_input], outputs=output)
model_base.compile(optimizer="adam",
                   loss="binary_crossentropy",
                   metrics=["accuracy"])
```

##  Explication des choix techniques

###  Tokenisation des URLs avec un `Tokenizer`
 **Pourquoi ?**  
Les URLs sont des **chaînes de caractères**, mais un modèle de deep learning a besoin de **données numériques**.  
Le **Tokenizer** transforme chaque mot/fréquence en un **indice unique**.

**Exemple :**

"https://secure-login.com" → [12, 8, 3, 6]



 **Paramètre clé** : `num_words=256`  
Seuls **les 256 mots les plus fréquents** sont retenus pour **réduire la complexité du modèle**.

---

### Encodage des labels avec `LabelEncoder`
**Pourquoi ?**  
Le modèle doit apprendre à classifier **4 types de labels** (**ou 6 si on inclut `XSS` et `Path Traversal`**).  
**`LabelEncoder` convertit les labels textuels (`benign`, `malware`, etc.) en indices numériques**.

**Exemple :**
benign → 0 malware → 1 phishing → 2 defacement → 3


---

### Pourquoi ces hyperparamètres ?

| **Paramètre**           | **Explication** |
|-------------------------|----------------|
| `input_dim=256`        | Seuls les **256 mots les plus fréquents** sont conservés pour la tokenisation. |
| `output_dim=64`        | La taille de l'embedding permet d'apprendre des **représentations denses** des tokens. |
| `LSTM(64)`            | Capture les **patterns dans la séquence URL**. 64 unités sont un bon compromis entre performance et complexité. |
| `Dense(32)` (features) | Capture les relations entre **caractéristiques tabulaires** (longueur, entropie, chiffres, etc.). |
| `Concatenate()`        | Fusionne les **deux flux d’informations** (**séquence URL + features tabulaires**). |
| `Dense(64) + Dropout(0.5)` | Ajoute une couche dense pour **affiner la classification** et réduit le **surapprentissage**. |
| `loss="binary_crossentropy"` | Fonction de perte adaptée à une classification **multi-classes one-hot encoded**. |
| `optimizer="adam"`     | Algorithme efficace pour l’**apprentissage en deep learning**. |

---

##  Évaluation des performances

Chaque essai possède ses propres **courbes d’évolution de l’entraînement** :

- **ESSAI1** *(Features et labels de base)*
- **ESSAI2** *(Features améliorés, labels de base)*
- **ESSAI3** *(Features de base, labels améliorés)*

 **Analyse globale** :
- Les modèles atteignent **90%+ de précision** après **20 epochs**.
- **ESSAI2** semble offrir **la meilleure stabilité**, tandis que **ESSAI3** capture **plus de menaces spécifiques** (`XSS`, `LFI`).
- **LSTM + Features Tabulaires** = **meilleure détection**.
