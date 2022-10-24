from scripts.fixtures_procedure import Fixture
from core.decorators import benchmark

@benchmark
def run():
    Fixture().create_fixture_empresas()
    Fixture().create_fixture_cuadrillas_tecnicas()
    Fixture().create_fixture_ciudades()
    Fixture().create_fixture_llamadas_tecnicas(5)
    Fixture().create_fixture_conexiones_completedworks()
    Fixture().create_fixture_reclamos_completedworks()
    Fixture().create_fixture_eventos_de_nodos()
    
    print("FIXTURES CREATION COMPLETED")