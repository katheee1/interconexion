import mysql.connector
import psycopg2

# --- Configuración de las conexiones ---
# ¡MUY IMPORTANTE! No pongas las contraseñas directamente en el código. 
# Utiliza variables de entorno o un método más seguro.

mysql_config = {
    "host": "localhost",
    "user": "root",
    "password": "",  # ¡Cuidado! No pongas contraseñas directamente en el código
    "database": "sakila"
}

postgres_config = {
    "host": "localhost",
    "database": "uniminuto",
    "user": "postgres",
    "password": "010803"  # ¡Cuidado! No pongas contraseñas directamente en el código
}

# --- Función para mostrar el contenido de una tabla ---
def mostrar_contenido_tabla(cursor, nombre_tabla, tipo_db):
    try:
        # Obtener información sobre las columnas de la tabla
        cursor.execute(f"DESCRIBE {nombre_tabla}" if tipo_db == "mysql" else f"SELECT column_name FROM information_schema.columns WHERE table_name = '{nombre_tabla}'")
        columnas = [col[0] for col in cursor.fetchall()]

        # Construir la consulta SELECT dinámicamente
        consulta = f"SELECT {', '.join(columnas)} FROM {nombre_tabla} LIMIT 10"  # LIMIT para evitar demasiados datos

        cursor.execute(consulta)
        datos = cursor.fetchall()

        print(f"\nContenido de la tabla '{nombre_tabla}' ({tipo_db}):")

        # Imprimir encabezados de columna
        print(" | ".join(columnas))
        print("-" * (len(" | ".join(columnas)) + 2))  # Línea separadora

        for fila in datos:
            # Convertir los valores a cadenas para evitar errores de formato
            fila_str = [str(valor) for valor in fila]
            print(" | ".join(fila_str))

    except Exception as e:
        print(f"Error al mostrar el contenido de la tabla '{nombre_tabla}' ({tipo_db}): {e}")

# --- Conexión y procesamiento de MySQL ---
try:
    mysql_conn = mysql.connector.connect(**mysql_config)
    print("Conexión exitosa a MySQL")
    mysql_cursor = mysql_conn.cursor()

    mysql_cursor.execute("SHOW TABLES")
    tablas_mysql = [tabla[0] for tabla in mysql_cursor.fetchall()]

    for tabla in tablas_mysql:
        mostrar_contenido_tabla(mysql_cursor, tabla, "mysql")

    mysql_cursor.close()
    mysql_conn.close()
    print("Conexión a MySQL cerrada")

except mysql.connector.Error as err:
    print(f"Error al conectar a MySQL: {err}")

# --- Conexión y procesamiento de PostgreSQL ---
try:
    postgres_conn = psycopg2.connect(**postgres_config)
    print("Conexión exitosa a PostgreSQL")
    postgres_cursor = postgres_conn.cursor()

    postgres_cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'")
    tablas_postgres = [tabla[0] for tabla in postgres_cursor.fetchall()]

    for tabla in tablas_postgres:
        mostrar_contenido_tabla(postgres_cursor, tabla, "postgres")

    postgres_cursor.close()
    postgres_conn.close()
    print("Conexión a PostgreSQL cerrada")

except psycopg2.Error as e:
    print(f"Error al conectar a PostgreSQL: {e}")




