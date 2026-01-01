"""Generate explicitly labeled synthetic calendar art in a NEW repository only."""
import argparse
from datetime import date, timedelta
import json
import os
from pathlib import Path
import subprocess

ROOT=Path(__file__).resolve().parent
START=date(2026,1,1)
END=date(2026,10,19)
GENERATED_ON='2026-10-20'


def git(*args, env=None):
    return subprocess.run(['git',*args],cwd=ROOT,env=env,check=True,capture_output=True,text=True).stdout.strip()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--author-name',required=True)
    parser.add_argument('--author-email',required=True)
    args=parser.parse_args()
    if (ROOT/'.git').exists():
        raise SystemExit('Refusing to change an existing Git repository.')
    parent_repo=subprocess.run(['git','-C',str(ROOT.parent),'rev-parse','--show-toplevel'],capture_output=True,text=True)
    if parent_repo.returncode==0:
        raise SystemExit('Refusing to create a repository nested in another Git repository.')
    git('init','-b','main')
    git('config','user.name',args.author_name)
    git('config','user.email',args.author_email)
    git('config','commit.gpgsign','false')
    lines=['synthetic_date,activity_type,actual_generation_date\n']
    day=START
    count=0
    while day<=END:
        lines.append(f'{day.isoformat()},synthetic_calendar_art,{GENERATED_ON}\n')
        (ROOT/'calendar.csv').write_text(''.join(lines),encoding='utf-8',newline='\n')
        env=os.environ.copy()
        env['GIT_AUTHOR_DATE']=f'{day.isoformat()}T12:00:00+06:00'
        # The committer date deliberately remains the actual generation time.
        env.pop('GIT_COMMITTER_DATE',None)
        git('add','README.md','.gitattributes','generate_calendar.py','calendar.csv')
        git('commit','-m',f'art: synthetic calendar entry for {day.isoformat()}',env=env)
        count+=1
        if count%50==0:
            print(f'Generated {count} explicitly labeled entries.',flush=True)
        day+=timedelta(days=1)
    actual=int(git('rev-list','--count','HEAD'))
    assert actual==count==(END-START).days+1==292
    assert len(lines)-1==count
    assert not git('status','--porcelain')
    print(json.dumps({'synthetic':True,'commits':count,'start':START.isoformat(),'end':END.isoformat(),'head':git('rev-parse','HEAD'),'working_tree':'clean'}))


if __name__=='__main__':
    main()
