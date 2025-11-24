import argparse
from engine.parser import ConfigParser
from engine.rule_engine import RuleEngine
from engine.generator import TemplateGenerator
from engine.validator import Validator
import shutil

def main(config_path: str, out_dir: str):
    parser = ConfigParser()
    cfg = parser.load(config_path)

    engine = RuleEngine()
    plan = engine.process(cfg)

    template_path = plan['template_path']
    gen = TemplateGenerator(template_path)
    shutil.rmtree(out_dir, ignore_errors=True)
    gen.generate(plan['modules'], plan['variables'], out_dir)

    print(f"Generated files in {out_dir}:")
    import os
    for f in sorted(os.listdir(out_dir)):
        print(' -', f)

    print('\\nRunning validation (requires terraform installed)...')
    val = Validator(out_dir)
    results = val.validate()
    for r in results:
        print('\\nCommand:', r['cmd'])
        print('Return code:', r['rc'])
        print('Stdout:\\n', r['out'])
        print('Stderr:\\n', r['err'])
    if results and results[-1]['rc'] == 0:
        print('\\nValidation passed: IaC is ready (dry-run recommended).')
    else:
        print('\\nValidation failed. See above outputs for details.')

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--config', default='examples/input_aws.json')
    ap.add_argument('--out', default='output')
    args = ap.parse_args()
    main(args.config, args.out)
