from coursedata.yaml_transformer import set_local
import hedy 

def test_import():
    set_local()
    assert hedy.local_keywords_enabled == True
    
    