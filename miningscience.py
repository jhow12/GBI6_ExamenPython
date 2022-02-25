from Bio import Entrez
import re
import pandas as pd

def download_pubmed(keyword):
    
    """ download_pubmed: se encarga de realizar una busqueda en la plataforma de PubMed deacuerdo a palabras claves encontradas
    en el articulo. Además nos lanza el numero de articulos encontrados
    keyword: Se refiere a palabras claves para la busqueda"""
    
    Entrez.email = "johanna.paez@est.ikiam.edu.ec"
    rec = Entrez.read(Entrez.esearch(db="pubmed", 
                            term=keyword,
                            usehistory="y"))
    webenv = rec["WebEnv"]
    query_key = rec["QueryKey"]
    handle = Entrez.efetch(db="pubmed",
                           rettype="medline", 
                           retmode="text", 
                           retstart=0,
                           retmax=543, webenv=webenv, query_key=query_key)
    dataKey = handle.read()
    Pubdata = re.sub(r'\n\s{6}','', dataKey)
    return Pubdata

    
def mining_pubs(tipo,archivo):
    """ mining_pubs es una funcion que ayuda a minar datos especificos dentro de un archivo determinado de Pubmed.
    la informacion que puede encontrar esta funcion es el autor es el nombre del autor, el año de publicacion y la ciudad/País del articulo.
    Si el tipo es "DP" recupera el año de publicación del artículo. El retorno es un dataframe con el PMID y el DP_year.
    Si el tipo es "AU" recupera el número de autores por PMID. El retorno es un dataframe con el PMID y el num_auth.
    Si el tipo es "AD" recupera el conteo de autores por país. El retorno es un dataframe con el country y el num_auth.
    El archivo: es el documento donde en donde se encuentra la data"""
    text = re.sub(r'\s+[Eceinlort]{10}\s+[aders]{7}.*','', archivo)
    text = re.sub(r'\s[\w._%+-]+@[\w.-]+\.[a-zA-Z]{1,4}','', text)
    text = re.sub(r'\..*\d.*\,',',', text)
    text1 = re.sub(r'\..*\d.*','', text)
    l=text1[1:].split('PMID-')
    ID=[]
    AU=[]
    DP=[]
    preAD=[]
    for PMID in l:
        x=PMID.split('\n')
        AUc=0
        ID.append(x[0])
        for fila in x:
            y=fila.split(' ')
            if y[0] == 'DP':
                DP.append(y[3])
            if y[0] == 'AU':
                AUc=AUc+1
            if y[0] == 'AD':
                w=fila.split(',')
                preAD.append(w[-1])
        AU.append(AUc)
    ID.pop(0)
    AU.pop(0)
    preAD.pop(-5)

    AP=[]
    for dire in preAD:
        b=dire
        c=dire.split(' ')
        if c[0] == 'AD':
            b=c[-1]   
        AP.append(b)

    s=0
    AC =[0]*len(AP)

    for obj in AP:
        bytes(obj,encoding="utf8")
        if obj != '.' or '':
            t=obj
            if t[0] == ' ':
                t = re.sub (r'^\s','',t)
            if t[-1] == '.':
                t = re.sub (r'\.$','',t)
            t = re.sub (r'\.$','',t)
        AC[s]=t
        s=s+1

    u=0
    AD=[0]*len(AP)
    for t in AC:
        if t == "USA":
            t='United States of America'
        if t == 'UK':
            t='United Kingdom'
        if t == "GA":
            t= 'Gabon'
        if t == 'CO':
            t='Colombia'
        if t == 'CA':
            t='Canada'
        AD[u]=t
        u=u+1
    Countries_molde=['Andorra','Afghanistan','Antigua and Barbuda','Anguilla','Albania','Armenia','The Netherlands','Angola','Antarctica','Argentina','American Samoa','Austria','Australia','Aruba','Azerbaijan','Bosnia and Herzegovina','Barbados','Bangladesh','Belgium','Burkina Faso','Bulgaria','Bahrain', 'Burundi','Benin','Bermuda','Brunei','Bolivia', 'Brazil','Bahamas','Bhutan','Bouvet Island','Botswana','Belarus','Belize','Canada','Cocos [Keeling] Islands','Congo [DRC]','Central African Republic','Congo [Republic]', 'Switzerland',"Côte d'Ivoire",'Cook Islands','Chile','Cameroon','China','Colombia','Costa Rica','Cuba', 'Cape Verde','Christmas Island','Cyprus','Czech Republic','Germany','Djibouti','Denmark','Dominica','Dominican Republic','Algeria','Ecuador' ,'Estonia','Egypt','Western Sahara','Eritrea','Spain','Ethiopia','Finland','Fiji','Falkland Islands [Islas Malvinas]','Micronesia','Faroe Islands','France','Gabon', 'United Kingdom','Grenada','Georgia','French Guiana','Guernsey','Ghana','Gibraltar','Greenland','Gambia', 'Guinea','Guadeloupe','Equatorial Guinea','Greece','South Georgia and the South Sandwich Islands','Guatemala','Guam','Guinea-Bissau','Guyana','Gaza Strip','Hong Kong','Heard Island and McDonald Islands','Honduras','Croatia', 'Haiti','Hungary','Indonesia','Ireland' ,'Israel','Isle of Man','India','British Indian Ocean Territory','Iraq', 'Iran','Iceland','Italy','Jersey','Jamaica','Jordan', 'Japan','Kenya','Kyrgyzstan','Cambodia','Kiribati','Comoros','Saint Kitts and Nevis','North Korea','South Korea','Kuwait','Cayman Islands','Kazakhstan','Laos','Lebanon','Saint Lucia','Liechtenstein','Sri Lanka','Liberia','Lesotho','Lithuania','Luxembourg','Latvia' ,'Libya','Morocco','Monaco','Moldova','Montenegro','Madagascar','Marshall Islands','Macedonia [FYROM]','Mali','Myanmar [Burma]','Mongolia' ,'Macau','Northern Mariana Islands','Martinique','Mauritania','Montserrat','Malta','Mauritius','Maldives','Malawi','Mexico','Malaysia' ,'Mozambique','Namibia','New Caledonia','Niger','Norfolk Island','Nigeria','Nicaragua','Netherlands','Norway','Nepal','Nauru','Niue','New Zealand','Oman','Panama','Peru','French Polynesia', 'Papua New Guinea','Philippines','Pakistan','Poland','Saint Pierre and Miquelon' ,'Pitcairn Islands','Puerto Rico','Palestinian Territories','Portugal','Palau','Paraguay','Qatar','Réunion','Romania','Serbia','Russia' ,'Rwanda','Saudi Arabia','Solomon Islands','Seychelles','Sudan','Sweden','Singapore','Saint Helena','Slovenia', 'Svalbard and Jan Mayen','Slovakia','Sierra Leone','San Marino','Senegal','Somalia','Suriname','São Tomé and Príncipe','El Salvador','Syria','Swaziland' ,'Turks and Caicos Islands','Chad','French Southern Territories','Togo','Thailand','Tajikistan','Tokelau','Timor-Leste','Turkmenistan' ,'Tunisia','Tonga','Turkey','Trinidad and Tobago','Tuvalu','Taiwan','Tanzania','Ukraine','Uganda','U.S. Minor Outlying Islands','United States of America','Uruguay','Uzbekistan','Vatican City','Saint Vincent and the Grenadines','Venezuela', 'British Virgin Islands','U.S. Virgin Islands','Vietnam','Vanuatu','Wallis and Futuna','Samoa','Kosovo','Yemen','Mayotte','South Africa','Zambia','Zimbabwe']

    o=AD
    f=Countries_molde
    i=len(f)
    ADh=[0]*i
    k=0
    for elem in f:
        d=0
        for comp in o:
            if elem == str(comp):
                d=d+1
        ADh[k]=d
        k=k+1


    AD=[]
    CO=[]
    n=0
    for elem in ADh:
        if str(elem) != '0':
            AD.append(elem)
            m=Countries_molde[n]
            CO.append(m)
        n=n+1

    TableA = pd.DataFrame({'PMID' : ID,
                           'Año' : DP})

    TableB = pd.DataFrame({'PMID' : ID,
                           'Autor' : AU})

    TableC = pd.DataFrame({'Country' : CO,
                           'Autor' : AD})
    
    if tipo =='DP':
        return TableA
    if tipo == 'AU':
        return TableB
    if tipo == 'AD':
        return TableC