"""Run all retailer scrapers sequentially."""
import sys


def run_all():
    from scraper.jumbo import extraer_productos_jumbo, cargar_productos_jumbo
    from scraper.carrefour import extraer_productos_carrefour, cargar_productos_carrefour
    from scraper.dia import extraer_productos_dia, cargar_productos_dia
    
    results = {}
    
    print("=" * 60)
    print("JUMBO")
    print("=" * 60)
    df_jumbo = extraer_productos_jumbo()
    if not df_jumbo.empty:
        inserted, updated = cargar_productos_jumbo(df_jumbo)
        results["jumbo"] = {"extracted": len(df_jumbo), "inserted": inserted, "updated": updated}
        print(f"Jumbo: {len(df_jumbo)} extraídos, {inserted} insertados, {updated} actualizados")
    
    print("\n" + "=" * 60)
    print("CARREFOUR")
    print("=" * 60)
    df_carrefour = extraer_productos_carrefour()
    if not df_carrefour.empty:
        inserted, updated = cargar_productos_carrefour(df_carrefour)
        results["carrefour"] = {"extracted": len(df_carrefour), "inserted": inserted, "updated": updated}
        print(f"Carrefour: {len(df_carrefour)} extraídos, {inserted} insertados, {updated} actualizados")
    
    print("\n" + "=" * 60)
    print("DIA")
    print("=" * 60)
    df_dia = extraer_productos_dia()
    if not df_dia.empty:
        inserted, updated = cargar_productos_dia(df_dia)
        results["dia"] = {"extracted": len(df_dia), "inserted": inserted, "updated": updated}
        print(f"Dia: {len(df_dia)} extraídos, {inserted} insertados, {updated} actualizados")
    
    print("\n" + "=" * 60)
    print("RESUMEN FINAL")
    print("=" * 60)
    for retailer, data in results.items():
        print(f"{retailer.upper()}: {data['extracted']} extraídos, {data['inserted']} insertados, {data['updated']} actualizados")
    
    total_extracted = sum(d["extracted"] for d in results.values())
    total_inserted = sum(d["inserted"] for d in results.values())
    total_updated = sum(d["updated"] for d in results.values())
    print(f"\nTOTAL: {total_extracted} extraídos, {total_inserted} insertados, {total_updated} actualizados")


if __name__ == "__main__":
    run_all()
