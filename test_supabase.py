from supabase import create_client, Client
import os

# Tus credenciales
SUPABASE_URL = "https://tu-proyecto-id.supabase.co"
SUPABASE_KEY = "tu-anon-key-aqui"

# Crear cliente
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Probar consulta
try:
    response = supabase.table('equipos').select("*").limit(5).execute()
    print("✅ Conexión exitosa!")
    print(f"Equipos encontrados: {len(response.data)}")
    print(response.data)
except Exception as e:
    print(f"❌ Error: {e}")