roles = ["auteur", "gestionnaire", "doyen", "vice-doyen", 'enseignant']

african_countries = [
    {"label": "Algérie", "code": "DZ", 'ordering': 1, 'nationality_label': 'Algérien'},
    {"label": "Angola", "code": "AO", 'ordering': 2, 'nationality_label': 'Angolais'},
    {"label": "Bénin", "code": "BJ", 'ordering': 3, 'nationality_label': 'Béninois'},
    {"label": "Botswana", "code": "BW", 'ordering': 4, 'nationality_label': 'Botswanais'},
    {"label": "Burkina Faso", "code": "BF", 'ordering': 5, 'nationality_label': 'Burkinabé'},
    {"label": "Burundi", "code": "BI", 'ordering': 6, 'nationality_label': 'Burundais'},
    {"label": "Cameroun", "code": "CM", 'ordering': 7, 'nationality_label': 'Camerounais'},
    {"label": "Cap-Vert", "code": "CV", 'ordering': 8, 'nationality_label': 'Cap-verdien'},
    {"label": "République centrafricaine", "code": "CF", 'ordering': 9, 'nationality_label': 'Centrafricain'},
    {"label": "Tchad", "code": "TD", 'ordering': 10, 'nationality_label': 'Tchadien'},
    {"label": "Comores", "code": "KM", 'ordering': 11, 'nationality_label': 'Comorien'},
    {"label": "République du Congo", "code": "CG", 'ordering': 12, 'nationality_label': 'Congolais'},
    {"label": "République démocratique du Congo", "code": "CD", 'ordering': 13, 'nationality_label': 'Congolais'},
    {"label": "Djibouti", "code": "DJ", 'ordering': 14, 'nationality_label': 'Djiboutien'},
    {"label": "Égypte", "code": "EG", 'ordering': 15, 'nationality_label': 'Égyptien'},
    {"label": "Guinée équatoriale", "code": "GQ", 'ordering': 16, 'nationality_label': 'Équatoguinéen'},
    {"label": "Érythrée", "code": "ER", 'ordering': 17, 'nationality_label': 'Érythréen'},
    {"label": "Éthiopie", "code": "ET", 'ordering': 18, 'nationality_label': 'Éthiopien'},
    {"label": "Gabon", "code": "GA", 'ordering': 19, 'nationality_label': 'Gabonais'},
    {"label": "Gambie", "code": "GM", 'ordering': 20, 'nationality_label': 'Gambien'},
    {"label": "Ghana", "code": "GH", 'ordering': 21, 'nationality_label': 'Ghanéen'},
    {"label": "Guinée", "code": "GN", 'ordering': 22, 'nationality_label': 'Guinéen'},
    {"label": "Guinée-Bissau", "code": "GW", 'ordering': 23, 'nationality_label': 'Bissau-Guinéen'},
    {"label": "Côte d'Ivoire", "code": "CI", 'ordering': 24, 'nationality_label': 'Ivoirien'},
    {"label": "Kenya", "code": "KE", 'ordering': 25, 'nationality_label': 'Kényan'},
    {"label": "Lesotho", "code": "LS", 'ordering': 26, 'nationality_label': 'Lésothien'},
    {"label": "Liberia", "code": "LR", 'ordering': 27, 'nationality_label': 'Libérien'},
    {"label": "Libye", "code": "LY", 'ordering': 28, 'nationality_label': 'Libyen'},
    {"label": "Madagascar", "code": "MG", 'ordering': 29, 'nationality_label': 'Malgache'},
    {"label": "Malawi", "code": "MW", 'ordering': 30, 'nationality_label': 'Malawien'},
    {"label": "Mali", "code": "ML", 'ordering': 31, 'nationality_label': 'Malien'},
    {"label": "Maroc", "code": "MA", 'ordering': 32, 'nationality_label': 'Marocain'},
    {"label": "Maurice", "code": "MU", 'ordering': 33, 'nationality_label': 'Mauricien'},
    {"label": "Mauritanie", "code": "MR", 'ordering': 34, 'nationality_label': 'Mauritanien'},
    {"label": "Mozambique", "code": "MZ", 'ordering': 35, 'nationality_label': 'Mozambicain'},
    {"label": "Namibie", "code": "NA", 'ordering': 36, 'nationality_label': 'Namibien'},
    {"label": "Niger", "code": "NE", 'ordering': 37, 'nationality_label': 'Nigérien'},
    {"label": "Nigeria", "code": "NG", 'ordering': 38, 'nationality_label': 'Nigérian'},
    {"label": "Ouganda", "code": "UG", 'ordering': 39, 'nationality_label': 'Ougandais'},
    {"label": "Rwanda", "code": "RW", 'ordering': 40, 'nationality_label': 'Rwandais'},
    {"label": "Sao Tomé-et-Principe", "code": "ST", 'ordering': 41, 'nationality_label': 'Santoméen'},
    {"label": "Sénégal", "code": "SN", 'ordering': 42, 'nationality_label': 'Sénégalais'},
    {"label": "Seychelles", "code": "SC", 'ordering': 43, 'nationality_label': 'Seychellois'},
    {"label": "Sierra Leone", "code": "SL", 'ordering': 44, 'nationality_label': 'Sierra-léonais'},
    {"label": "Somalie", "code": "SO", 'ordering': 45, 'nationality_label': 'Somalien'},
    {"label": "Afrique du Sud", "code": "ZA", 'ordering': 46, 'nationality_label': 'Sud-africain'},
    {"label": "Soudan", "code": "SD", 'ordering': 47, 'nationality_label': 'Soudanais'},
    {"label": "Soudan du Sud", "code": "SS", 'ordering': 48, 'nationality_label': 'Soudanais du Sud'},
    {"label": "Swaziland", "code": "SZ", 'ordering': 49, 'nationality_label': 'Swazilandais'},
    {"label": "Tanzanie", "code": "TZ", 'ordering': 50, 'nationality_label': 'Tanzanien'},
    {"label": "Togo", "code": "TG", 'ordering': 51, 'nationality_label': 'Togolais'},
    {"label": "Tunisie", "code": "TN", 'ordering': 52, 'nationality_label': 'Tunisien'},
    {"label": "Zambie", "code": "ZM", 'ordering': 53, 'nationality_label': 'Zambien'},
    {"label": "Zimbabwe", "code": "ZW", 'ordering': 54, 'nationality_label': 'Zimbabwéen'},
]

congo_cities = [
        {"label": "Brazzaville", "country": "Congo", "code": 'BZ', 'ordering': 1},
        {"label": "Pointe-Noire", "country": "Congo", "code": 'PN', 'ordering': 2},
        {"label": "Dolisie", "country": "Congo", "code": 'DL', 'ordering': 3},
        {"label": "Nkayi", "country": "Congo", "code": 'NK', 'ordering': 4},
        {"label": "Owando", "country": "Congo", "code": 'OW', 'ordering': 5},
        {"label": "Gamboma", "country": "Congo", "code": 'GM', 'ordering': 7},
        {"label": "Impfondo", "country": "Congo", "code": 'IM', 'ordering': 8},
        {"label": "Sibiti", "country": "Congo", "code": 'SI', 'ordering': 9},
        {"label": "Mossendjo", "country": "Congo", "code": 'MO', 'ordering': 10},
        {"label": "Kinkala", "country": "Congo", "code": 'KI', 'ordering': 11},
        {"label": "Mindouli", "country": "Congo", "code": 'MLI', 'ordering': 12},
        {"label": "Ewo", "country": "Congo", "code": 'EWO', 'ordering': 13},
        {"label": "Madingou", "country": "Congo", "code": 'MNG', 'ordering': 14},
        {"label": "Oyo", "country": "Congo", "code": 'OYO', 'ordering': 15},
        {"label": "Ouesso", "country": "Congo", "code": 'OSO', 'ordering': 16},
        {"label": "Goma Tsé-Tsé", "country": "Congo", "code": 'GTT', 'ordering': 17},
        {"label": "Kindamba", "country": "Congo", "code": 'KBA', 'ordering': 18},
        {"label": "Loutété", "country": "Congo", "code": 'LTT', 'ordering': 19},
        {"label": "Makabana", "country": "Congo", "code": 'MKB', 'ordering': 20},
        {"label": "Mossaka", "country": "Congo", "code": 'MSK', 'ordering': 21},
        {"label": "Boko", "country": "Congo", "code": 'BKO', 'ordering': 22},
        {"label": "Etoumbi", "country": "Congo", "code": 'ETB', 'ordering': 23},
        {"label": "Mbanza-Ndounga", "country": "Congo", "code": 'MZA', 'ordering': 24},
        {"label": "Ngo", "country": "Congo", "code": 'NGO', 'ordering': 26},
        {"label": "Tchamba-Mbamba", "country": "Congo", "code": 'TCH', 'ordering': 27},
        {"label": "Zanaga", "country": "Congo", "code": 'ZGA', 'ordering': 28},
    ]