"""Validate final exports, source agreement, numbering, and evidence counts."""
from pathlib import Path
import re,json,collections,importlib.util,hashlib
from pypdf import PdfReader
from docx import Document
from docx.oxml.ns import qn

BASE=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('builder',BASE/'source/build_package.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
blocks=json.loads((BASE/'source/thesis-content.json').read_text());refs=b.number_items(blocks)
d=Document(BASE/'thesis.docx');actual=collections.Counter(p.text for p in d.paragraphs)
assert all(actual[b.prose(t,refs)] for k,t in blocks if k=='p')
assert all(b.texprose(t) in (BASE/'latex/main.tex').read_text() for k,t in blocks if k=='p')
assert d.styles['Normal'].font.size.pt==11
assert d.sections[0]._sectPr.find(qn('w:pgNumType')).get(qn('w:fmt'))=='lowerRoman'
assert d.sections[1]._sectPr.find(qn('w:pgNumType')).get(qn('w:start'))=='1'

def roman(n):
 s=''
 for v,c in [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),(50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]:
  while n>=v:s+=c;n-=v
 return s

stats={}
for name in ['thesis.pdf','thesis-latex.pdf','conference-paper.pdf','conference-paper-latex.pdf']:
 r=PdfReader(BASE/name);texts=[p.extract_text() for p in r.pages]
 assert all(abs(float(p.mediabox.width)-612)<1 and abs(float(p.mediabox.height)-792)<1 for p in r.pages)
 assert not any('??' in t or 'Fields update when opened' in t for t in texts)
 assert all(len(t.split())>4 for t in texts)
 latex='latex' in name
 if name.startswith('thesis'):
  start=next(i for i,t in enumerate(texts) if any(line.strip()=='Chapter 1: Introduction' for line in t.splitlines()))
  reference=next(i for i,t in enumerate(texts[start:],start) if any(line.strip()=='References' for line in t.splitlines()))
  assert 45<=reference-start<=55
  for i,t in enumerate(texts):
   lines=[line.strip() for line in t.splitlines() if line.strip()]
   number=lines[-1] if latex else lines[0]
   assert number==(roman(i+1) if i<start else str(i-start+1)),(name,i+1,number)
  stats[name]={'total_pages':len(r.pages),'preliminary_pages':start,'main_text_pages':reference-start,'first_main_physical_page':start+1}
 else:
  assert 6<=len(r.pages)<=8
  stats[name]={'total_pages':len(r.pages),'layout':'two columns with full-width tables'}

# Validate every cached navigation entry against the actual Arabic body pages.
r=PdfReader(BASE/'thesis.pdf');txt=[p.extract_text() for p in r.pages]
start=stats['thesis.pdf']['preliminary_pages'];norm=lambda s:re.sub('[^a-z0-9]','',s.lower())
nav=json.loads((BASE/'qa/navigation-pages.json').read_text())
for title,page,*_ in nav['contents']+nav['figures']+nav['tables']:
 needle=norm(title)
 # Figure lists abbreviate the caption at its first sentence.
 assert needle in norm(txt[start+page-1]),('wrong navigation',title,page)

for key,n in {('0.8b','lora1-off'):65,('0.8b','lora1-limit512'):67,('2b','lora1-off'):165,('2b','lora1-limit1024'):191,('4b','lora1-off'):300,('4b','lora1-limit2048'):332}.items():
 assert b.S[key]['coverage']==b.S[key]['attempts']==464
 assert abs(b.S[key]['accuracy']-n/464)<1e-12
for fn in ['main','conference']:
 log=(BASE/'latex'/(fn+'.log')).read_text()
 assert 'Overfull' not in log
 assert 'undefined references' not in log and 'Citation' not in log
stats['evidence_checks']={'unique_test_ids':len(set(b.DATA['problem_ids'])),'complete_combinations':6,'figures_in_thesis':sum(k=='figure' for k,t in blocks),'tables_in_thesis':sum(k=='table' for k,t in blocks),'references':len(refs),'shared_body_prose_matches':True,'latex_compilation':'successful; no overfull boxes or unresolved citations/references'}
(BASE/'qa/final-validation.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
