def test_rule_process():
    from engine.rule_engine import RuleEngine
    cfg = {'provider':'aws','region':'us-east-1','resources':{}}
    r = RuleEngine().process(cfg)
    assert 'template_path' in r
    assert 'variables' in r
