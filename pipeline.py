import json
from pathlib import Path

def apply_events(events):
    state={};positions={};ignored=[]
    for event in events:
        key=str(event['key']);seq=int(event['lsn'])
        if seq<=positions.get(key,-1):ignored.append(seq);continue
        positions[key]=seq
        if event['op']=='d':state.pop(key,None)
        elif event['op'] in {'c','u','r'}:state[key]=event['after']
        else:raise ValueError('Unknown CDC op: '+event['op'])
    return {'records':state,'positions':positions,'ignored_lsn':ignored}

def run(source,destination):
    result=apply_events([json.loads(line) for line in Path(source).read_text().splitlines() if line.strip()]);Path(destination).write_text(json.dumps(result,indent=2));return result
