"""Publish the checked 464-problem study throughout the Markdown documentation.

Keep original Markdown in the dated archive and raw run reports unchanged.
Current theses/tables are rebuilt; earlier notes get explicit scope and current links.
This script reads saved scores only. It never runs models or generated answers.
"""
import argparse
import hashlib
import json
import os
import re
import subprocess
import tarfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = ROOT/'archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz'
START, END = '<!-- CURRENT-STUDY:START -->', '<!-- CURRENT-STUDY:END -->'
LABEL = {'off':'Thinking OFF','on':'Thinking ON','brief':'Think briefly',
         'lora1':'LoRA-1 alone (ON)','lora2':'LoRA-2 (ON)',
         **{f'limit{n}':f'Limit {n:,}' for n in (512,1024,2048,4096)},
         'lora1-off':'LoRA-1 + OFF',
         **{f'lora1-limit{n}':f'LoRA-1 + limit {n:,}' for n in (512,1024,2048)}}


def pct(value):
    return f'{100*value:.1f}%'


def table(headers,rows):
    return '\n'.join(['| '+' | '.join(headers)+' |','|'+'|'.join('---' for _ in headers)+'|']+
        ['| '+' | '.join(map(str,row))+' |' for row in rows])+'\n'


def relative(source,target):
    return os.path.relpath(ROOT/target,(ROOT/source).parent)


def rebase(text,source,destination):
    def link(match):
        target=match.group(2)
        if re.match(r'[a-z]+:',target) or target.startswith('#'):
            return match.group(0)
        path,sep,anchor=target.partition('#')
        full=(ROOT/source).parent/path
        return match.group(1)+'('+os.path.relpath(full,(ROOT/destination).parent)+(sep+anchor if sep else '')+')'
    return re.sub(r'(!?\[[^\]]*\])\(([^)]+)\)',link,text)


def strip_notice(text):
    return re.sub(re.escape(START)+r'.*?'+re.escape(END)+r'\n*','',text,flags=re.S)


def notice(path,historical=False):
    details=('**Historical record below.** Its earlier scores, model choices and plans describe that stage only.\n'
             'Use the current results linked here for the completed study.\n\n') if historical else ''
    return START+'\n\n'+details+'''**Current study — 14 October 2026:** **464 unique test problems**.
Benchmarks: **164 HumanEval+**, **166 LiveCodeBench easy**, **134 LiveCodeBench medium**.
All six planned LoRA combinations are complete, one attempt per problem:

- **0.8B:** LoRA + OFF **14.0% (65/464)**; LoRA + limit 512 **14.4% (67/464)**.
- **2B:** LoRA + OFF **35.6% (165/464)**; LoRA + limit 1,024 **41.2% (191/464)**.
- **4B:** LoRA + OFF **64.7% (300/464)**; LoRA + limit 2,048 **71.6% (332/464)**.

LoRA alone means thinking ON without a thinking-token limit.
Older methods' all-attempt averages and first-attempt comparisons are labelled separately.
LoRA + OFF does not consistently improve on free OFF; the 2B/4B gains over free limits remain uncertain.

'''+f'[Every method, benchmark, difficulty, token count and interval]({relative(path,"results/CURRENT-RESULTS.md")}) · '+f'[Full easy thesis]({relative(path,"easy-thesis/FULL-THESIS.md")}) · '+f'[Full formal Markdown thesis]({relative(path,"thesis/THESIS.md")}).\n\n'+END+'\n\n'


def add_notice(path,text,historical=False):
    text=strip_notice(text)
    # Preserve model-card YAML front matter and the document's title.
    start=0
    if text.startswith('---\n'):
        end=text.find('\n---',4)
        if end>=0:start=end+4
    title=re.search(r'^# .+\n',text[start:],re.M)
    index=start+title.end() if title else start
    return text[:index].rstrip()+'\n\n'+notice(path,historical)+text[index:].lstrip()


def is_raw_report(path):
    return '/completed-464/' in path or '/completed40/' in path


def write(path,text):
    (ROOT/path).parent.mkdir(parents=True,exist_ok=True)
    (ROOT/path).write_text(text.rstrip()+'\n')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
    if args.check:
        return check()
    data=json.loads((ROOT/'results/combined/results.json').read_text())
    assert data['total_problems']==464 and len(data['summaries'])==26
    assert not data['audit']['exact_id_overlap']
    with tarfile.open(ARCHIVE) as original:
        original_background=original.extractfile('thesis/02-background.md').read().decode()
        original_references=original.extractfile('thesis/08-references.md').read().decode()
    easy=lambda name:strip_notice((ROOT/'easy-thesis'/name).read_text())
    current=easy('05-results.md')
    write('results/CURRENT-RESULTS.md',rebase(current.replace('# The combined results','# Current results — every saved method and benchmark',1),
        'easy-thesis/05-results.md','results/CURRENT-RESULTS.md')+'''
## Source of truth and scope

This page includes all 26 saved model/configuration pairs, including partial methods.
Every percentage comes from saved graded results, not a replacement of old raw scores.
There are 464 unique test IDs and 13,980 saved attempts across all methods and sizes.
The eight immutable downloaded Markdown reports remain alongside their original raw answers.
Their scope is recorded in the [complete documentation audit](DOCUMENTATION-AUDIT.md).
The dated archive preserves the pre-update text of every original Markdown document.
Use current Markdown for the latest thesis. Older PDF/HTML exports have not been rebuilt.

Rebuild all current Markdown after updating checked results:

```sh
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
python3 scripts/sync_thesis_markdown.py
python3 scripts/sync_thesis_markdown.py --check
```
''')
    # Rewrite current formal chapters; retain original versions in the dated archive.
    chapters={
        '00-front-matter.md':'''# Stop Overthinking, Keep Passing the Tests

## Shortest-Correct LoRA Training and Free Thinking Controls in Qwen3.5-0.8B, 2B and 4B

**Author:** [your name] · **Supervisor:** [supervisor's name] · **[University], [Department]**

Updated 14 October 2026. Retrospective combined analysis of **464 unique code problems**.
The original protocol and the current combined study are distinguished throughout.

## Abstract

We compared saved code-generation results for three Qwen3.5 model sizes.
The test set contains 164 HumanEval+ and 300 LiveCodeBench problems.
Each problem has equal weight; each method reports its actual coverage.
We compared thinking ON, OFF, thinking limits, prompting, and trained LoRA add-ons.
All six LoRA + OFF/limit combinations now cover the same 464 problems.
The 2B LoRA + limit 1,024 combination passed 191/464 problems (41.2%).
The 4B LoRA + limit 2,048 combination passed 332/464 (71.6%).
For 0.8B, OFF without training remains the highest observed full-set score (14.7%).
The 2B and 4B combinations do not establish a reliable accuracy gain over free limits.
The earlier LoRA-2 and loop findings retain their actual 234-problem scope.
This does not establish that all training methods fail or that one setting is universally best.

'''+easy('00-one-page.md'),
        '01-introduction.md':easy('02-the-problem.md'),
        '02-background.md':original_background.replace('Our model, Qwen3.5-2B, has about',
            'The original core model, Qwen3.5-2B, has about')+'\n## Scope of the completed extension\n\nThe current study also includes Qwen3.5-0.8B and Qwen3.5-4B.\nThe background and cited literature explain the original motivation.\nCurrent empirical claims use the checked 464-problem result tables.\n',
        '03-method.md':easy('03-how-we-did-it.md')+'\n\n'+easy('04-the-datasets.md'),
        '04-how-we-measure.md':'# Measurement and uncertainty\n\n'+'## How accuracy is calculated'+easy('03-how-we-did-it.md').split('## How accuracy is calculated',1)[1]+'\n\n'+easy('WORDS.md'),
        '05-results.md':current,
        '06-analysis.md':easy('06-why-it-works.md')+'\n\n'+easy('11-completed-lora-controls.md'),
        '07-conclusion-and-future-work.md':easy('07-advice-and-limits.md')+'\n\n## Conclusion from all six completed combinations\n\n'+
            easy('11-completed-lora-controls.md').split('## Practical conclusion',1)[1].split('## Reproduce without GPU spending',1)[0],
        '08-references.md':original_references+'\n## Scope of these references\n\nThis is the existing literature catalogue, retained from the original study.\nThis results update did not repeat a web or publication audit.\nCurrent measurements and run provenance are linked in the results and appendices.\n',
    }
    for name,text in chapters.items():
        # Original background/reference links already originate in thesis/.
        source='thesis/'+name if name in ('02-background.md','08-references.md') else 'easy-thesis/'+name
        write('thesis/'+name,rebase(text,source,'thesis/'+name))
    problems=json.loads((ROOT/'results/lora-controls-inputs/problem-templates.json').read_text())['problems']
    rows=[[p['task_id'],'HumanEval+' if p['source']=='humaneval' else 'LiveCodeBench',p['difficulty']] for p in sorted(problems,key=lambda p:p['task_id'])]
    appendix='''# Appendices: the completed study

## Every test problem

All 464 frozen test IDs appear below. Training and pilot problems are excluded.
The 234/40/190 collection history is documented in the method, not treated as separate headline studies.

'''+table(['Test ID','Benchmark','Difficulty'],rows)+'''
## Every available problem-level score and source

- [Per-problem scores and token means](../results/combined/per-problem.csv).
- [Every graded source file and original pass count](../results/combined/sources.csv).
- [Combined scores, intervals and training-ID audit](../results/combined/results.json).
- [All benchmark and difficulty tables](../results/CURRENT-RESULTS.md).
- [Checked new run configurations and first-attempt comparisons](../results/lora-controls/checked-results.json).
- [Saved raw answers and run notes](../results/lora-controls/README.md).
- [Original LoRA-2 training-problem table](../results/full-results/tables/training-problems.csv).

The last table describes the original 280-problem training pool, not extra test problems.
Training/test exact-ID overlap is zero. This does not prove no text or pretraining exposure.
LoRA-2 and historical loop findings were not extended to 464 problems.
No missing result is counted as a failure. Partial-method denominators remain visible.

## Reproduce all current Markdown, without GPU work

```sh
.venv/bin/python scripts/audit_lora_controls.py
python3 scripts/combine_results.py
python3 scripts/build_combined_easy_thesis.py
python3 scripts/sync_thesis_markdown.py
python3 scripts/sync_thesis_markdown.py --check
```

Do not rerun completed notebooks merely to rebuild the text.
Notebook 23 is superseded by Notebook 24. No completed configuration needs repeating.

## Historical versions and export status

[Original Markdown snapshot](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz)
contains every pre-update Markdown document, including the original formal thesis.
Raw CSV/JSONL and downloaded reports retain their original contents.
Existing PDF and HTML exports are historical; this update refreshes Markdown only.
'''
    write('thesis/09-appendices.md',appendix)
    write('thesis/README.md','''# The updated thesis

Read [THESIS.md](THESIS.md) for the full formal Markdown thesis.
The [easy thesis](../easy-thesis/FULL-THESIS.md) uses the same checked results.
Both include all six completed LoRA combinations and every saved benchmark/configuration.

[All result tables](../results/CURRENT-RESULTS.md) · [Documentation audit](../results/DOCUMENTATION-AUDIT.md).

The chapters contain the motivation, background, method, datasets, measurement,
all results, interpretation, limitations, references, and all 464 test IDs.
First-attempt results and all-attempt problem averages are labelled separately.
Partial sweeps, the pilot, LoRA-2 and loop findings keep their actual coverage.

## Rebuild

Run `python3 scripts/sync_thesis_markdown.py` after rebuilding the easy thesis.
The full command sequence is in the appendices. It uses no GPU calls.
Edit generators or source chapters rather than the joined THESIS.md file.

## Export status

The existing PDF and HTML files are older exports. They have not been refreshed.
Use current Markdown for this completed 464-problem study.
The dated archive preserves all earlier Markdown, including the original thesis.
''')
    # Replace reader-facing result aggregates instead of leaving old headlines current.
    for path in ['results/ALL-RESULTS.md','results/SIZE-COMPARISON.md','results/full-results/FULL-RESULTS.md']:
        write(path,rebase((ROOT/'results/CURRENT-RESULTS.md').read_text(),'results/CURRENT-RESULTS.md',path))
    for model in ('0.8b','4b'):
        rows=[s for s in data['summaries'] if s['model']==model]
        text=f'# {model.upper()}: all saved configurations\n\nAccuracy uses all saved attempts, with equal weight per problem.\nFirst-attempt comparisons are separately labelled in the complete result page.\n\n'
        text+=table(['Way','Accuracy','Coverage','Attempts','Mean thinking tokens','Mean total tokens'],[
            [LABEL[s['method']],pct(s['accuracy']),f'{s["coverage"]}/464',s['attempts'],f'{s["thinking_tokens"]:,.0f}',f'{s["total_new_tokens"]:,.0f}'] for s in rows])
        text+='\n'+table(['Way','Benchmark','Difficulty','Coverage','Accuracy'],[
            [LABEL[s['method']],g['source'],g['difficulty'],g['coverage'],pct(g['accuracy'])] for s in rows for g in s['groups']])
        text+='\n[Every benchmark, comparisons and intervals](../CURRENT-RESULTS.md).\nOriginal raw cohort files are unchanged; their earlier summary text is preserved in the dated archive.\n'
        write(f'results/{model}/SUMMARY.md',text)
    write('TEACHER-A-TO-Z.md','# Teacher guide: the completed 464-problem thesis\n\n'+
        rebase(easy('08-all-answers.md')+'\n\n'+easy('11-completed-lora-controls.md'),'easy-thesis/08-all-answers.md','TEACHER-A-TO-Z.md'))
    write('qa/51-all-markdown-current.md','''# Updating every thesis-related Markdown file

The earlier update covered the easy thesis, but left the formal thesis and older summaries stale.
We audited every Markdown file, rebuilt the current theses, and labelled historical notes.

## What changed?

Both full theses now show all saved configurations and benchmark groups.
The main result pages and model summaries use current scores.
Earlier proposals, Q&A, lessons and run notes show a current-study notice and retain their original context.
The original Markdown files are preserved in a dated archive.
Raw answer files, grades, model weights and downloaded reports are unchanged.

## Why keep older numbers anywhere?

A 234-problem result is a real historical result, not an error to replace with a 464-problem score.
Its scope must stay clear. Missing results cannot be invented or treated as failures.
Current first-attempt comparisons must not be mixed with all-attempt averages.

## Are all benchmark settings complete?

The six planned LoRA combinations each cover all 464 problems.
Some older limit sweeps and LoRA-2 remain partial; the current tables show their actual coverage.
No claim is made that every possible setting was tested.

## Checked and not run

Every Markdown path has a disposition in the documentation audit.
The eight downloaded run reports are byte-checked and preserved, with current links from their parent pages.
The project rules file remains an instruction file. The decision log is append-only.
The audit checks notices, current results, local links, raw report hashes and the formal/easy result text.
No model generation, training or paid compute was used. Existing PDF/HTML exports are not refreshed.

[Complete audit](../results/DOCUMENTATION-AUDIT.md) · [Current tables](../results/CURRENT-RESULTS.md) ·
[Full easy thesis](../easy-thesis/FULL-THESIS.md) · [Full formal thesis](../thesis/THESIS.md).
''')
    decisions=ROOT/'DECISIONS.md'
    if '| 113 |' not in decisions.read_text():
        decisions.write_text(decisions.read_text()+'''\n| 113 | 2026-10-14 | **Synchronize all thesis-related Markdown.** Rebuild the formal thesis and aggregate result pages from the checked 464-problem analysis; add current-study links and explicit scope to earlier notes. Keep immutable downloaded reports and raw scores byte-identical. Preserve every original Markdown document in a dated archive and list every file in a documentation audit. | User explicitly requested every related Markdown file, including the older thesis, be updated without omissions. The formal thesis is now current; the archive retains its earlier study. No new model run is needed. | `results/DOCUMENTATION-AUDIT.md` · `results/CURRENT-RESULTS.md` · `qa/51-all-markdown-current.md` |\n''')
    qindex=ROOT/'qa/README.md'
    if '51-all-markdown-current.md' not in qindex.read_text():
        qindex.write_text(qindex.read_text()+'\n- [51 — Every thesis-related Markdown file reviewed and synchronized](51-all-markdown-current.md).\n')
    current_paths={'README.md','PLAN.md','ROADMAP.md','TEACHER-A-TO-Z.md','PAPERS.md','GLOSSARY.md',
        'qa/README.md','qa/50-completed-lora-controls.md','qa/51-all-markdown-current.md',
        'results/lora-controls/README.md','results/lora-missing40/README.md','results/lora-limit-2b/README.md',
        'results/RESULTS-INDEX.md','results/combined/README.md','results/CURRENT-RESULTS.md',
        'results/ALL-RESULTS.md','results/SIZE-COMPARISON.md','results/full-results/FULL-RESULTS.md',
        'results/0.8b/SUMMARY.md','results/4b/SUMMARY.md','results/DOCUMENTATION-AUDIT.md'}
    entries=[]
    for file in sorted(ROOT.rglob('*.md')):
        path=str(file.relative_to(ROOT))
        if any(part.startswith('.') or part in ('node_modules','archive') for part in file.relative_to(ROOT).parts):continue
        if path=='CLAUDE.md':
            entries.append((path,'Instruction file; preserved, not a results document'));continue
        if path=='DECISIONS.md':
            entries.append((path,'Append-only decision log; current update in decision 113'));continue
        if is_raw_report(path):
            entries.append((path,'Immutable downloaded report; original scope, current parent-page links'));continue
        if path=='thesis/THESIS.md':continue  # Rebuilt from checked chapters below.
        historical=not (path in current_paths or path.startswith(('easy-thesis/','thesis/')))
        text=file.read_text()
        if not historical:
            text=text.replace('The formal thesis retains its historical results.',
                'The formal Markdown thesis is also updated; its original version is preserved in the dated archive.')
            text=text.replace('The formal thesis and old project stages remain historical.',
                'The formal Markdown thesis is updated. Earlier project stages remain historical.')
            text=text.replace('The original protocol and formal thesis remain historical;',
                'The original protocol remains historical; both Markdown theses are now updated;')
            text=text.replace('The [original formal thesis](thesis/THESIS.md) and raw files preserve the historical study.',
                'The [formal Markdown thesis](thesis/THESIS.md) is current. The dated archive and raw files preserve the original study.')
        write(path,add_notice(path,text,historical))
        entries.append((path,'Historical/teaching/research context retained; current results and scope added' if historical
            else 'Current results/chapter/index; synchronized and linked'))
    subprocess.run(['node','scripts/build_thesis.js'],cwd=ROOT,check=True)
    path='thesis/THESIS.md';write(path,add_notice(path,(ROOT/path).read_text()))
    entries.append((path,'Current full formal thesis; rebuilt from all updated chapters'))
    # Include this audit itself so the inventory has no implicit omissions.
    entries=[row for row in entries if row[0]!='results/DOCUMENTATION-AUDIT.md']
    entries.append(('results/DOCUMENTATION-AUDIT.md','Complete Markdown inventory and validation report'))
    entries.sort()
    audit='''# Complete thesis Markdown audit — 14 October 2026

The earlier update did not update every older thesis document. This audit closes that gap.
Both full Markdown theses, aggregate results and model summaries now use the checked 464-problem study.
Historical notes show current results and explicitly retain their earlier scope.
Every saved method, benchmark and difficulty appears in [the current tables](CURRENT-RESULTS.md).
Partial methods remain partial; missing answers are not invented or scored as failures.

## Coverage of this audit

'''+f'**{len(entries)} Markdown files reviewed**, including this audit.\n\n'+'''
- Current theses and result tables: rebuilt or synchronized.
- Earlier Q&A, proposals, lessons and run notes: current notice plus explicit historical/teaching scope.
- Eight downloaded run reports: immutable original evidence, checked against archived hashes.
- `CLAUDE.md`: project instructions, preserved.
- `DECISIONS.md`: append-only; the current change is recorded in decision 113.
- PDF/HTML files are outside this Markdown update and remain older exports.

The [dated original snapshot](../archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz)
contains all 157 Markdown documents present before synchronization.
Raw JSONL, CSV, weights and downloaded reports were not edited.
The older 234-problem loop/LoRA-2 analyses and pilot are retained with their true scope.

## Every file and its disposition

'''+table(['Markdown file','How it is handled'],[[f'[{path}]({relative("results/DOCUMENTATION-AUDIT.md",path)})',status] for path,status in entries])+'''
## Validation

Run `python3 scripts/sync_thesis_markdown.py --check`.
It checks inventory coverage, current notices, all six combination scores, source-table consistency,
local current-document links, immutable report hashes, and the formal/easy results match.
The current dataset has 464 unique test IDs, with zero exact overlap against saved training IDs.
Generated code and model inference were not executed during this documentation work.
'''
    write('results/DOCUMENTATION-AUDIT.md',add_notice('results/DOCUMENTATION-AUDIT.md',audit))
    write('results/documentation-audit.json',dict_to_json({'files':[dict(path=p,status=s) for p,s in entries],
        'markdown_count':len(entries),'original_snapshot':'archive/2026-10-14-before-complete-md-sync/markdown-originals.tar.gz'}))
    check()


def dict_to_json(value):
    return json.dumps(value,indent=2)+'\n'


def check():
    audit=json.loads((ROOT/'results/documentation-audit.json').read_text())
    inventory={row['path']:row['status'] for row in audit['files']}
    files={str(p.relative_to(ROOT)) for p in ROOT.rglob('*.md')
        if not any(part.startswith('.') or part in ('node_modules','archive') for part in p.relative_to(ROOT).parts)}
    assert files==set(inventory),(files-set(inventory),set(inventory)-files)
    snapshot=json.loads((ARCHIVE.parent/'manifest.json').read_text())
    raw_count=0
    for path in files:
        text=(ROOT/path).read_text()
        if is_raw_report(path):
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==snapshot['files'][path],path
            raw_count+=1;continue
        if path=='CLAUDE.md':
            assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest()==snapshot['files'][path];continue
        if path=='DECISIONS.md':
            assert '| 113 |' in text;continue
        assert text.count(START)==text.count(END)==1,(path,'missing/duplicate current notice')
        for score in ('65/464','67/464','165/464','191/464','300/464','332/464'):
            assert score in text,(path,score)
        # Validate links introduced by the notice, plus all links in rewritten current documents.
        link_text=text[text.index(START):text.index(END)]
        if path.startswith(('thesis/','easy-thesis/')) or path in ('results/CURRENT-RESULTS.md','results/DOCUMENTATION-AUDIT.md'):
            link_text=text
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',link_text):
            if re.match(r'[a-z]+:',target) or target.startswith('#'):continue
            assert ((ROOT/path).parent/target.split('#')[0]).exists(),(path,target)
    assert raw_count==8,raw_count
    source=strip_notice((ROOT/'easy-thesis/05-results.md').read_text()).strip()
    formal=strip_notice((ROOT/'thesis/05-results.md').read_text()).strip()
    assert rebase(source,'easy-thesis/05-results.md','thesis/05-results.md')==formal
    for needle in ('LoRA-1 + limit 512','LoRA-1 + limit 1,024','LoRA-1 + limit 2,048',
                   'Every benchmark and difficulty: all available methods','Every benchmark and difficulty: first attempts'):
        assert needle in source,needle
    print(f'Checked every Markdown path: {len(files)} reviewed, {len(files)-10} current notices, 8 immutable reports, 2 instruction/decision files.')


if __name__=='__main__':
    main()
