#!/usr/bin/env python3
import os, sys
import pandas as pd
import mysql.connector
import unicodedata
import math

# --- DEBUG INICIAL ---
print("Python:", sys.executable)
print("CWD   :", os.getcwd())

# --- RUTA AL CSV ---
if len(sys.argv) > 1:
    csv_path = sys.argv[1]
else:
    # Fallback a la ruta original si no se proporciona ningún argumento
    csv_path = os.path.expanduser(
        "~/Desktop/MIS PROYECTOS/CADBRIOEX/CRM-CABRIOEX/CRM Cadbioex V2.0 - limpio (1).csv"
    )
assert os.path.exists(csv_path), f"No se encuentra el archivo CSV en: {csv_path}"

# --- 1) LEER Y LIMPIAR NaNs ---
df = pd.read_csv(
    csv_path,
    sep=';',
    header=3,
    encoding='latin1',
    dtype=str,
    engine='python'
)
df = df.iloc[:, :16].fillna('')  # recorta a 16 cols y NaN→''

# --- 2) RENOMBRAR COLUMNAS ---
df.columns = [
    'CLIENTE','NIF','POBLACION','DIRECCION','TELEFONO','CORREO',
    'PUESTA_EN_MARCHA','MARCA','MODELO','N_SERIE','GARANTIA',
    'SERVICIO','FECHA','AÑO','MES','OBSERVACION'
]

# --- 3) NORMALIZAR (tildes, espacios, mayúsculas) + limpiar literales 'NAN' ---
def normalizar_serie(serie):
    return (
        serie.astype(str)
             .str.strip()
             .str.upper()
             .map(lambda x: unicodedata.normalize('NFKD', x)
                               .encode('ascii','ignore')
                               .decode('ascii'))
    )
for col in df.columns:
    df[col] = normalizar_serie(df[col])
df.replace('NAN', '', inplace=True)

# --- 4) PREPARAR clientes_df y eliminar duplicados ---
clientes_df = df[[
    'CLIENTE','NIF','POBLACION','DIRECCION','TELEFONO','CORREO'
]].copy()

# --- Lógica para separar Nombre y Apellidos ---
# Esta función intenta resolver la ambigüedad entre nombres compuestos y apellidos compuestos.
def split_name_logic(full_name):
    parts = full_name.strip().split()
    num_words = len(parts)
    
    if num_words >= 4: # ej: Adela Maria Vargas Velarde
        name = " ".join(parts[:-2])
        surname = " ".join(parts[-2:])
    elif num_words == 3: # ej: Adela Maria Vargas
        name = " ".join(parts[:-1])
        surname = parts[-1]
    elif num_words == 2: # ej: Juan Perez (y Adela Maria)
        name = parts[0]
        surname = parts[1]
    elif num_words == 1: # ej: Maria
        name = parts[0]
        surname = ""
    else:
        name = ""
        surname = ""
    return pd.Series([name, surname])

# Aplicar la lógica a la columna CLIENTE
clientes_df[['nombre', 'apellido']] = clientes_df['CLIENTE'].apply(split_name_logic)

# Asignar el resto de columnas
clientes_df['nif'] = clientes_df['NIF']
clientes_df['poblacion'] = clientes_df['POBLACION']
clientes_df['direccion'] = clientes_df['DIRECCION']
clientes_df['telefono'] = clientes_df['TELEFONO']
clientes_df['email'] = clientes_df['CORREO']

# Añadir columnas vacías
clientes_df['provincia'] = ''
clientes_df['codigo_postal'] = ''

# Seleccionar y reordenar las columnas finales, eliminando las originales en mayúsculas
cli_cols = ['nombre', 'apellido', 'nif', 'provincia', 'poblacion', 'direccion', 'codigo_postal', 'telefono', 'email']
clientes_df = clientes_df[cli_cols]


# eliminar duplicados en Python
clientes_df = clientes_df.drop_duplicates(subset=['nif'], keep='first')
clientes_df = clientes_df.drop_duplicates(subset=['nombre'], keep='first')

# --- 5) PREPARAR equipos_df ---
# Tomamos las columnas de equipo
equipos_df = df[[
    'NIF','MARCA','MODELO','N_SERIE','GARANTIA',
    'PUESTA_EN_MARCHA','MES','OBSERVACION'
]].copy()
# Filtrar solo filas con número de serie no vacío
equipos_df = equipos_df[equipos_df['N_SERIE'].str.strip() != '']
# Eliminar duplicados de acuerdo a NIF + serie
equipos_df = equipos_df.drop_duplicates(['NIF','N_SERIE'])
# Renombrar columnas según esquema de BBDD
equipos_df.rename(columns={
    'NIF':'nif',
    'MARCA':'marca',
    'MODELO':'modelo',
    'N_SERIE':'n_serie',
    'OBSERVACION':'comentario'
}, inplace=True)
# Mapear campos adicionales
equipos_df['garantia']       = equipos_df['GARANTIA'].map(lambda x: 1 if x=='SI' else 0)
equipos_df['meses_garantia'] = equipos_df['MES'].map(lambda x: int(x) if x.isdigit() else None)
equipos_df['compra_biomex']  = 0
equipos_df['fecha_compra']   = equipos_df['PUESTA_EN_MARCHA']
# Columnas para insertar
eq_cols = [
    'id_Clientes','marca','modelo','n_serie',
    'garantia','meses_garantia','compra_biomex','fecha_compra','comentario'
]

# --- 6) CONEXIÓN A MySQL y TRUNCATE ---
db_cfg = {'host':'localhost','user':'root','password':'Calamonte.1994','database':'bd_cadbioex'}
cnx = mysql.connector.connect(**db_cfg)
cur = cnx.cursor()
# Vaciar tablas para volcado limpio
cur.execute("SET FOREIGN_KEY_CHECKS=0;")
cur.execute("TRUNCATE TABLE servicios;")
cur.execute("TRUNCATE TABLE equipos;")
cur.execute("TRUNCATE TABLE clientes;")
cur.execute("SET FOREIGN_KEY_CHECKS=1;")
cnx.commit()
print("Tablas servicios, equipos y clientes vaciadas.")

# --- 7) INSERCIÓN DE CLIENTES ---
print("Iniciando inserción de clientes...")
cli_sql = f"INSERT IGNORE INTO clientes ({','.join(cli_cols)}) VALUES ({','.join(['%s']*len(cli_cols))})"
cli_vals = [tuple(row[col] for col in cli_cols) for _, row in clientes_df.iterrows()]
cur.executemany(cli_sql, cli_vals)
cnx.commit()
print(f"→ {cur.rowcount} clientes INSERT/IGNORED")
# Mapeo NIF→id_Clientes
cur.execute("SELECT id_Clientes,nif FROM clientes")
mapa_cli = {nif: cid for cid, nif in cur.fetchall()}

# --- 8) INSERCIÓN DE EQUIPOS ---
print("Iniciando inserción de equipos...")
eq_sql = f"INSERT IGNORE INTO equipos ({','.join(eq_cols)}) VALUES ({','.join(['%s']*len(eq_cols))})"
eq_vals = []
for _, r in equipos_df.iterrows():
    cid = mapa_cli.get(r['nif'])
    if not cid: continue
    raw = [cid, r['marca'], r['modelo'], r['n_serie'], r['garantia'], r['meses_garantia'], r['compra_biomex'], r['fecha_compra'], r['comentario']]
    clean = [None if (v is None or (isinstance(v, float) and math.isnan(v))) else v for v in raw]
    eq_vals.append(tuple(clean))
cur.executemany(eq_sql, eq_vals)
cnx.commit()
print(f"→ {cur.rowcount} equipos INSERT/IGNORED")

# --- 9) INSERCIÓN DE SERVICIOS ---
print("Iniciando inserción de servicios...")
servicios_df = df[['NIF','N_SERIE','SERVICIO','FECHA','AÑO','MES','OBSERVACION']].dropna(subset=['SERVICIO','FECHA']).copy()
servicios_df.rename(columns={'NIF':'nif','N_SERIE':'n_serie','OBSERVACION':'comentario'}, inplace=True)
tipo_map = {'PUESTA EN MARCHA':1,'1¼ LIMPIEZA':2}
servicios_df['tipo_servicio'] = servicios_df['SERVICIO'].map(lambda s: tipo_map.get(s,0))
servicios_df['fecha_servicio'] = servicios_df['FECHA']
servicios_df['anio_servicio'] = servicios_df['AÑO'].map(lambda x: int(x) if x.isdigit() else None)
servicios_df['mes_servicio'] = servicios_df['MES'].map(lambda x: int(x) if x.isdigit() else None)
servicios_df['trabajador'] = ''
servicios_df['horas'] = None
# Mapeo a id_Equipos
cur.execute("SELECT id_Equipos,id_Clientes,n_serie FROM equipos")
equipo_map = {(cid,nserie):eid for eid,cid,nserie in cur.fetchall()}
serv_cols = ['id_Equipo','tipo_servicio','fecha_servicio','anio_servicio','mes_servicio','trabajador','horas','comentario']
serv_sql = f"INSERT INTO servicios ({','.join(serv_cols)}) VALUES ({','.join(['%s']*len(serv_cols))})"
serv_vals = []
for _, r in servicios_df.iterrows():
    cid = mapa_cli.get(r['nif'])
    eid = equipo_map.get((cid, r['n_serie']))
    if not cid or not eid:
        continue
    raw = [eid, r['tipo_servicio'], r['fecha_servicio'], r['anio_servicio'], r['mes_servicio'], r['trabajador'], r['horas'], r['comentario']]
    clean = []
    for v in raw:
        if v is None or (isinstance(v, float) and math.isnan(v)) or (isinstance(v, str) and v.strip().lower()=='nan'):
            clean.append(None)
        else:
            clean.append(v)
    serv_vals.append(tuple(clean))
if serv_vals:
    cur.executemany(serv_sql, serv_vals)
    cnx.commit()
    print(f"→ {cur.rowcount} servicios INSERTED")
else:
    print("→ Sin servicios a insertar")

# --- 10) CIERRE ---
cur.close()
cnx.close()
print("✅ Volcado completo con todas las columnas del Excel.")

