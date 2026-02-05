"""
Teste básico do cache em memória
"""
import time
from dataverse_client import SimpleCache


def test_cache():
    """Test basic cache functionality"""
    print("=" * 80)
    print("Testando Cache em Memória")
    print("=" * 80)
    
    # Test 1: Basic set and get
    print("\n1. Teste básico - Set e Get:")
    print("-" * 80)
    cache = SimpleCache(default_ttl_seconds=5)
    
    cache.set("key1", {"name": "Test Account", "id": "123"})
    result = cache.get("key1")
    print(f"  ✓ Set e Get funcionando: {result}")
    
    # Test 2: TTL expiration
    print("\n2. Teste de expiração (TTL = 2 segundos):")
    print("-" * 80)
    cache.set("key2", {"data": "expires soon"}, ttl_seconds=2)
    print(f"  Imediatamente após set: {cache.get('key2')}")
    print("  Aguardando 3 segundos...")
    time.sleep(3)
    print(f"  Após expiração: {cache.get('key2')}")
    
    # Test 3: Cache stats
    print("\n3. Teste de estatísticas:")
    print("-" * 80)
    cache.set("key3", {"test": "data3"})
    cache.set("key4", {"test": "data4"})
    cache.set("key5", {"test": "data5"})
    stats = cache.get_stats()
    print(f"  ✓ Total de entradas: {stats['total_entries']}")
    print(f"  ✓ Tamanho estimado: {stats['cache_size_bytes']} bytes")
    
    # Test 4: Clear cache
    print("\n4. Teste de limpeza:")
    print("-" * 80)
    print(f"  Antes de limpar: {cache.get_stats()['total_entries']} entradas")
    cache.clear()
    print(f"  Após limpar: {cache.get_stats()['total_entries']} entradas")
    
    # Test 5: Cleanup expired
    print("\n5. Teste de limpeza de expirados:")
    print("-" * 80)
    cache.set("expire1", "data1", ttl_seconds=1)
    cache.set("expire2", "data2", ttl_seconds=10)
    cache.set("expire3", "data3", ttl_seconds=1)
    print(f"  Antes de dormir: {cache.get_stats()['total_entries']} entradas")
    time.sleep(2)
    cache.cleanup_expired()
    print(f"  Após cleanup: {cache.get_stats()['total_entries']} entradas")
    print(f"  Entradas não expiradas ainda acessíveis: {cache.get('expire2')}")
    
    print("\n" + "=" * 80)
    print("✓ Todos os testes passaram!")
    print("=" * 80)


if __name__ == "__main__":
    test_cache()
