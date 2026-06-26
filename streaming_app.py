import pyodbc

# Conexión a la base de datos
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 18 for SQL Server};'
    'SERVER=localhost,1433;'
    'DATABASE=STREAMING_EDUCATIVO;'
    'UID=sa;'
    'PWD=TuPassword123!;'
    'TrustServerCertificate=yes;'
)
cursor = conn.cursor()

def menu():
    while True:
        print("\n===== STREAMING EDUCATIVO =====")
        print("1. Ver todas las tablas")
        print("2. Insertar registro")
        print("3. Eliminar registro")
        print("4. Actualizar registro")
        print("5. Consultas avanzadas")
        print("6. Salir")
        opcion = input("Elige una opción: ")

        if opcion == "1":
            ver_tablas()
        elif opcion == "2":
            insertar()
        elif opcion == "3":
            eliminar()
        elif opcion == "4":
            actualizar()
        elif opcion == "5":
            consultas_avanzadas()
        elif opcion == "6":
            print("Hasta luego!")
            break
        else:
            print("Opción inválida.")

def ver_tablas():
    tablas = ["USUARIO", "PLANES", "CONTENIDO", "EPISODIO", "SUSCRIPCION", "HISTORIAL", "FAVORITOS"]
    for tabla in tablas:
        print(f"\n--- {tabla} ---")
        cursor.execute(f"SELECT * FROM {tabla}")
        for fila in cursor.fetchall():
            print(fila)

def insertar():
    print("\n¿Qué deseas insertar?")
    print("1. Usuario")
    print("2. Contenido")
    opcion = input("Elige: ")
    
    if opcion == "1":
        print("\n--- Usuarios actuales ---")
        cursor.execute("SELECT * FROM USUARIO")
        for fila in cursor.fetchall():
            print(fila)
        nombre = input("Nombre: ")
        correo = input("Correo: ")
        password = input("Password: ")
        fecha = input("Fecha nacimiento (YYYY-MM-DD): ")
        cursor.execute("INSERT INTO USUARIO (nombre, correo, password, fecha_nacimiento) VALUES (?,?,?,?)", 
                      nombre, correo, password, fecha)
        conn.commit()
        print("\n✅ Usuario insertado!")
        print("\n--- Usuarios actualizados ---")
        cursor.execute("SELECT * FROM USUARIO")
        for fila in cursor.fetchall():
            print(fila)

    elif opcion == "2":
        print("\n--- Contenido actual ---")
        cursor.execute("SELECT * FROM CONTENIDO")
        for fila in cursor.fetchall():
            print(fila)
        titulo = input("Título: ")
        tipo = input("Tipo (Documental/Tutorial/Podcast): ")
        categoria = input("Categoría: ")
        anio = input("Año: ")
        edad = input("Clasificación edad: ")
        cursor.execute("INSERT INTO CONTENIDO (titulo, tipo, categoria, anio, clasificacion_edad) VALUES (?,?,?,?,?)",
                      titulo, tipo, categoria, anio, edad)
        conn.commit()
        print("\n✅ Contenido insertado!")
        print("\n--- Contenido actualizado ---")
        cursor.execute("SELECT * FROM CONTENIDO")
        for fila in cursor.fetchall():
            print(fila)

def eliminar():
    print("\n¿Qué deseas eliminar?")
    print("1. Usuario")
    print("2. Contenido")
    opcion = input("Elige: ")

    if opcion == "1":
        cursor.execute("SELECT usuario_id, nombre FROM USUARIO")
        for fila in cursor.fetchall():
            print(fila)
        id = input("ID del usuario a eliminar: ")
        confirm = input(f"¿Seguro que deseas eliminar el usuario {id}? (s/n): ")
        if confirm == "s":
            try:
                cursor.execute("DELETE FROM USUARIO WHERE usuario_id = ?", id)
                conn.commit()
                print("✅ Usuario eliminado!")
            except Exception as e:
                print(f"❌ No se puede eliminar: tiene registros relacionados.")
                conn.rollback()

    elif opcion == "2":
        cursor.execute("SELECT contenido_id, titulo FROM CONTENIDO")
        for fila in cursor.fetchall():
            print(fila)
        id = input("ID del contenido a eliminar: ")
        confirm = input(f"¿Seguro que deseas eliminar el contenido {id}? (s/n): ")
        if confirm == "s":
            try:
                cursor.execute("DELETE FROM CONTENIDO WHERE contenido_id = ?", id)
                conn.commit()
                print("✅ Contenido eliminado!")
            except Exception as e:
                print(f"❌ No se puede eliminar: tiene registros relacionados.")
                conn.rollback()

def actualizar():
    print("\n¿Qué deseas actualizar?")
    print("1. Usuario")
    print("2. Contenido")
    opcion = input("Elige: ")

    if opcion == "1":
        cursor.execute("SELECT usuario_id, nombre FROM USUARIO")
        for fila in cursor.fetchall():
            print(fila)
        id = input("ID del usuario a actualizar: ")
        nombre = input("Nuevo nombre: ")
        correo = input("Nuevo correo: ")
        cursor.execute("UPDATE USUARIO SET nombre=?, correo=? WHERE usuario_id=?", nombre, correo, id)
        conn.commit()
        print("✅ Usuario actualizado!")
        cursor.execute("SELECT * FROM USUARIO")
        for fila in cursor.fetchall():
            print(fila)

    elif opcion == "2":
        cursor.execute("SELECT contenido_id, titulo FROM CONTENIDO")
        for fila in cursor.fetchall():
            print(fila)
        id = input("ID del contenido a actualizar: ")
        titulo = input("Nuevo título: ")
        tipo = input("Nuevo tipo: ")
        cursor.execute("UPDATE CONTENIDO SET titulo=?, tipo=? WHERE contenido_id=?", titulo, tipo, id)
        conn.commit()
        print("✅ Contenido actualizado!")
        cursor.execute("SELECT * FROM CONTENIDO")
        for fila in cursor.fetchall():
            print(fila)

def consultas_avanzadas():
    print("\n===== CONSULTAS AVANZADAS =====")
    
    print("\n1. Top 3 usuarios con más contenido en favoritos:")
    cursor.execute("""
        SELECT TOP 3 U.nombre, COUNT(F.contenido_id) AS total_favoritos
        FROM USUARIO U JOIN FAVORITOS F ON U.usuario_id = F.usuario_id
        GROUP BY U.nombre 
        ORDER BY total_favoritos DESC;
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n2. Contenido más visto (por historial):")
    cursor.execute("""
        SELECT C.titulo, COUNT(H.episodio_id) AS vistas
        FROM CONTENIDO C JOIN EPISODIO E ON C.contenido_id = E.contenido_id
        JOIN HISTORIAL H ON E.episodio_id = H.episodio_id
        GROUP BY C.titulo ORDER BY vistas DESC
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n3. Visualizaciones en enero y mayo:")
    cursor.execute("""
        SELECT U.nombre, C.titulo, H.fecha_visualizacion
        FROM HISTORIAL H
        JOIN USUARIO U ON H.usuario_id = U.usuario_id
        JOIN EPISODIO E ON H.episodio_id = E.episodio_id
        JOIN CONTENIDO C ON E.contenido_id = C.contenido_id
        WHERE MONTH(H.fecha_visualizacion) IN (1, 5)
        ORDER BY H.fecha_visualizacion
    """)
    for fila in cursor.fetchall():
        print(fila)

    print("\n4. Consulta libre - Usuarios con suscripción activa y su plan:")
    cursor.execute("""
        SELECT U.nombre, P.nombre AS nombre_plan, S.fecha_inicio, S.fecha_fin
        FROM USUARIO U 
        JOIN SUSCRIPCION S ON U.usuario_id = S.usuario_id
        JOIN PLANES P ON S.plan_id = P.plan_id
        WHERE EXISTS (SELECT 1 FROM SUSCRIPCION S2 
                     WHERE S2.usuario_id = U.usuario_id 
                     AND S2.estado = 'activa')
        ORDER BY P.nombre
    """)
    for fila in cursor.fetchall():
        print(fila)

menu()
