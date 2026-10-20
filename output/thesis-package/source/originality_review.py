"""Limited, transparent local overlap review; not a commercial plagiarism score."""
from pathlib import Path
import re,json,collections,html,subprocess,importlib.util,concurrent.futures
from pypdf import PdfReader

BASE=Path(__file__).resolve().parents[1]
sp=importlib.util.spec_from_file_location('builder',BASE/'source/build_package.py');b=importlib.util.module_from_spec(sp);sp.loader.exec_module(b)
blocks=json.loads((BASE/'source/thesis-content.json').read_text())
paragraphs=[t for k,t in blocks if k=='p']
def words(s):return re.findall(r'[a-z0-9]+',s.lower())
def grams(s,n=12):
 w=words(s);return {tuple(w[i:i+n]) for i in range(max(0,len(w)-n+1))}
main='\n'.join(paragraphs);g=grams(main)
reference=Path('/Users/mahmudqudrati/Downloads/A_Thesis_Report_updated_formatted.pdf')
reftext='\n'.join(p.extract_text() for p in PdfReader(reference).pages)
shared=g & grams(reftext)
duplicates=[{'count':n,'text':p} for p,n in collections.Counter(paragraphs).items() if n>1]
sentences=re.split(r'(?<=[.!?])\s+',main)
repeated_sentences=[{'count':n,'text':s} for s,n in collections.Counter(sentences).items() if n>1 and len(words(s))>=15]

def check_source(item):
 key,(_,title,year,url)=item
 try:
  p=subprocess.run(['curl','-L','--fail','--silent','--max-time','25',url],capture_output=True,text=True,check=True)
  doc=p.stdout
  m=re.search(r'<blockquote[^>]*class="abstract[^>]*>(.*?)</blockquote>',doc,re.S)
  if m:
   sample=html.unescape(re.sub('<[^>]+>',' ',m[1]));scope='abstract'
  else:
   m=re.search(r'<meta[^>]*name="description"[^>]*content="([^"]+)"',doc)
   sample=html.unescape(m[1]) if m else '';scope='page description'
  return {'key':key,'url':url,'title':title,'scope':scope,'sample_words':len(words(sample)),'matching_12_word_sequences':len(g & grams(sample)),'fetch':'ok' if sample else 'no abstract extracted'}
 except Exception as e:return {'key':key,'url':url,'fetch':'unavailable','reason':str(e)[:160]}

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:sources=list(pool.map(check_source,b.REFERENCES.items()))
audit={'method':'Exact normalized contiguous 12-word sequence comparison; body prose only','reference_pdf_pages':len(PdfReader(reference).pages),'reference_shared_sequences':len(shared),'reference_examples':[' '.join(x) for x in sorted(shared)[:5]],'duplicate_paragraphs':duplicates,'repeated_sentences':repeated_sentences,'primary_source_abstract_checks':sources}
(BASE/'qa/originality-audit.json').write_text(json.dumps(audit,indent=2))
lines=['# Originality review','Reviewed 20 October 2026. This is a limited editorial and textual-overlap review, not a Turnitin or iThenticate report.','## Checks performed',f'The main thesis prose was compared with all {audit["reference_pdf_pages"]} pages of the supplied misinformation-detection PDF using exact normalized sequences of 12 consecutive words. Headings, captions, references, and tables were excluded from the manuscript comparison.',f'Found {len(shared)} shared 12-word sequences against that PDF. This is a narrow exact-text result, not a percentage estimate of plagiarism.',f'Found {len(duplicates)} exactly duplicated body paragraphs and {len(repeated_sentences)} repeated sentences of at least 15 words. Necessary repetition of method names, figures, and numerical results is not itself evidence of copying.','The 13 references were checked against primary publisher, arXiv, or official model-card pages. Titles and citation years use the linked records. A small set of exact-phrase web searches was also reviewed; it is not an exhaustive web search.','## Accessible primary-source samples']
for s in sources:
 lines.append('- '+s['key']+': '+s['fetch']+('; '+s.get('scope','')+', '+str(s.get('sample_words',0))+' words checked, '+str(s.get('matching_12_word_sequences',0))+' shared 12-word sequences' if s['fetch']=='ok' else '')+'. '+s['url'])
lines+=['## Interpretation and remaining work','The sample checks cover accessible abstracts or page descriptions, not full-text comparison with every cited paper. Exact-word matching cannot detect paraphrased copying, translated copying, private sources, or unattributed ideas. No certified similarity percentage is claimed.','The thesis and conference paper intentionally share the same study and some author-created explanation. They should not be submitted as unrelated studies. The original repository supplied project evidence and existing drafts; this package is an expanded rewrite of that same work, not a claim of independent new experiments.','Before institutional submission, complete the marked author and institutional details, have the authors verify every scientific claim, and run the institution\x27s required similarity service if applicable.']
(BASE/'originality-review.md').write_text('\n\n'.join(lines)+'\n')
print('Reference shared 12-word sequences:',len(shared),'Duplicate paragraphs:',len(duplicates),'Repeated sentences:',len(repeated_sentences))
print('Primary samples checked:',sum(s['fetch']=='ok' for s in sources),'of',len(sources))
