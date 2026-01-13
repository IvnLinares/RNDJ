#!/usr/bin/env python3
"""
Script de prueba para los endpoints de perfil
"""
import urllib.request
import json

BASE_URL = "http://localhost:8000/api/v1"

# Credenciales del usuario de prueba creado anteriormente
TEST_USER = {
    "username": "juan_scout",
    "password": "Password123!"
}

def make_request(method, endpoint, data=None, token=None):
    """Realiza una petición HTTP"""
    url = f"{BASE_URL}{endpoint}"
    
    headers = {
        'Content-Type': 'application/json'
    }
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    json_data = json.dumps(data).encode('utf-8') if data else None
    
    request = urllib.request.Request(
        url,
        data=json_data,
        headers=headers,
        method=method
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read()), response.status, None
    except urllib.error.HTTPError as e:
        try:
            error_data = json.loads(e.read())
        except:
            error_data = {"error": str(e)}
        return None, e.code, error_data

def test_endpoints():
    print("=" * 60)
    print("🧪 PRUEBAS DE ENDPOINTS DE PERFIL")
    print("=" * 60)
    
    # 1. Login
    print("\n1️⃣ PRUEBA: Login")
    print("-" * 60)
    
    # Preparar datos de login en formato form-data
    from urllib.parse import urlencode
    form_data = urlencode({
        'username': TEST_USER['username'],
        'password': TEST_USER['password']
    }).encode('utf-8')
    
    request = urllib.request.Request(
        f"{BASE_URL}/auth/login",
        data=form_data,
        headers={'Content-Type': 'application/x-www-form-urlencoded'},
        method='POST'
    )
    
    try:
        with urllib.request.urlopen(request) as response:
            login_data = json.loads(response.read())
            token = login_data.get('access_token')
            print(f"✅ Login exitoso")
            print(f"   Token: {token[:20]}...")
    except urllib.error.HTTPError as e:
        print(f"❌ Error al hacer login: {e.reason}")
        error = json.loads(e.read())
        print(f"   Detalle: {error.get('detail')}")
        return
    
    # 2. GET /users/me - Obtener perfil actual
    print("\n2️⃣ PRUEBA: GET /users/me (Obtener perfil)")
    print("-" * 60)
    
    response, status, error = make_request('GET', '/users/me', token=token)
    
    if response:
        print(f"✅ Perfil obtenido (Status: {status})")
        user = response
        print(f"   ID: {user.get('id')}")
        print(f"   Username: {user.get('username')}")
        print(f"   Email: {user.get('email')}")
        print(f"   Nombre: {user.get('full_name')}")
        print(f"   Grupo: {user.get('scout_group')}")
        print(f"   Región: {user.get('scout_region')}")
        print(f"   Rango: {user.get('scout_rank')}")
        print(f"   Puntos: {user.get('points')}")
        print(f"   Nivel: {user.get('level')}")
        print(f"   Insignias: {user.get('badges_count')}")
    else:
        print(f"❌ Error al obtener perfil (Status: {status})")
        print(f"   Detalle: {error}")
        return
    
    # 3. PUT /users/me - Actualizar perfil
    print("\n3️⃣ PRUEBA: PUT /users/me (Actualizar perfil)")
    print("-" * 60)
    
    update_data = {
        "full_name": "Juan Carlos Pérez García",
        "scout_group": "Grupo Scout Central - Actualizado",
        "scout_region": "Región Centro Sur",
        "scout_rank": "Pionero"
    }
    
    response, status, error = make_request('PUT', '/users/me', update_data, token)
    
    if response:
        print(f"✅ Perfil actualizado (Status: {status})")
        updated_user = response
        print(f"   Nombre: {updated_user.get('full_name')}")
        print(f"   Grupo: {updated_user.get('scout_group')}")
        print(f"   Región: {updated_user.get('scout_region')}")
        print(f"   Rango: {updated_user.get('scout_rank')}")
    else:
        print(f"❌ Error al actualizar perfil (Status: {status})")
        print(f"   Detalle: {error}")
        return
    
    # 4. GET /users/{id} - Obtener perfil de usuario específico
    print("\n4️⃣ PRUEBA: GET /users/{id} (Obtener perfil por ID)")
    print("-" * 60)
    
    user_id = user.get('id')
    response, status, error = make_request('GET', f'/users/{user_id}', token=token)
    
    if response:
        print(f"✅ Perfil obtenido (Status: {status})")
        fetched_user = response
        print(f"   ID: {fetched_user.get('id')}")
        print(f"   Username: {fetched_user.get('username')}")
        print(f"   Nombre: {fetched_user.get('full_name')}")
    else:
        print(f"❌ Error al obtener perfil (Status: {status})")
        print(f"   Detalle: {error}")
    
    # 5. GET /users - Listar todos los usuarios
    print("\n5️⃣ PRUEBA: GET /users (Listar usuarios)")
    print("-" * 60)
    
    response, status, error = make_request('GET', '/users?limit=5', token=token)
    
    if response:
        print(f"✅ Usuarios obtenidos (Status: {status})")
        users_list = response
        print(f"   Total obtenidos: {len(users_list)}")
        for idx, u in enumerate(users_list[:3], 1):
            print(f"   {idx}. {u.get('username')} ({u.get('email')})")
    else:
        print(f"❌ Error al obtener usuarios (Status: {status})")
        print(f"   Detalle: {error}")
    
    print("\n" + "=" * 60)
    print("✅ TODAS LAS PRUEBAS COMPLETADAS")
    print("=" * 60)

if __name__ == '__main__':
    test_endpoints()
