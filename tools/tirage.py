"""Tire des milliers de questions d'un module HTML et cherche les questions fausses ou ambiguës.

Usage :
    python tools/tirage.py modules/<id>.html               # 2000 tirages par compétence et niveau
    python tools/tirage.py --tirages 500 --exemples 5 modules/<id>.html

Pourquoi : les questions d'un module HTML sont tirées au hasard par des générateurs JS écrits par
un LLM. Relire le code ne suffit pas : une combinaison rare peut donner deux bonnes réponses, un
choix en double ou un « undefined » à l'écran. On fait tourner les vrais générateurs de la page
(avec node, sans navigateur) et on vérifie chaque question tirée :
- une seule bonne réponse, présente parmi les choix ; pas de valeur ni de libellé en double ;
- pas de « undefined », « NaN », « null » ou « [object Object] » dans le texte ;
- la compétence et le niveau de la question sont ceux demandés, et existent dans la fiche ;
- les fiches Apprendre s'affichent, et leur petite question a une bonne réponse.
Avertissement (ne bloque pas) : un mauvais choix sans « pourquoi », une compétence sans générateur.
On affiche aussi quelques exemples par compétence et niveau, à relire : l'outil voit les erreurs
de forme, pas une réponse fausse sur le fond (un calcul faux reste « une seule bonne réponse »).

La page doit suivre docs/gabarit-module.html : questions faites par Q() et C(), et, à la fin du
script, la ligne qui donne { GEN, LEVELS, LEARN, SKILLS, EVAL_SKILLS } à window.__miniprofTirage.
Sortie : 0 si aucune erreur, 1 sinon, 2 si node est introuvable ou si la page ne se charge pas.
"""

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from check_html import Rapport, lire_fiche

SCRIPT = re.compile(r"<script>(.*?)</script>", re.DOTALL)

# Faux navigateur minimal : la page ne fait que préparer ses écrans avant d'appeler le tirage.
# Tout objet du DOM est remplacé par un « bouchon » qui accepte n'importe quel appel.
HARNAIS = r"""
'use strict';
const bouchon=()=>new Proxy(function(){},{
  get:(t,k)=>k===Symbol.toPrimitive?(()=>''):(k==='innerHTML'||k==='textContent'?'':bouchon()),
  apply:()=>bouchon(),set:()=>true});
globalThis.document=bouchon();globalThis.location={};
globalThis.requestAnimationFrame=()=>0;
const PARAM=__PARAM__;
let appele=false;
globalThis.window={scrollTo(){},matchMedia:()=>({matches:false}),addEventListener(){},
  __miniprofTirage:api=>{appele=true;verifier(api);}};
const out={erreurs:{},avertissements:{},exemples:{},tirages:0,niveaux:[]};
const texte=s=>String(s).replace(/<svg[\s\S]*?<\/svg>/g,'[dessin]').replace(/<[^>]+>/g,' ')
  .replace(/&nbsp;/g,' ').replace(/&lt;/g,'<').replace(/&gt;/g,'>').replace(/&amp;/g,'&').replace(/\s+/g,' ').trim();
// Une erreur par sorte et par endroit, avec le nombre de fois et un exemple
function note(table,ou,msg,ex){const k=ou+' : '+msg;const e=table[k]||(table[k]={n:0,ex:ex||''});e.n++;}
const MOTS_INTERDITS=/undefined|NaN|\[object Object\]|\bnull\b/;
function verifierQuestion(q,k,lv,ou){
  if(!q||typeof q!=='object'||!Array.isArray(q.choices)||!q.exp){note(out.erreurs,ou,'question sans choices ni exp : faire la question avec Q()');return;}
  const vs=q.choices.map(c=>String(c.v)),ls=q.choices.map(c=>texte(c.label));
  const ex=texte(q.prompt)+' ['+ls.join(' / ')+']';
  if(q.skill!==k)note(out.erreurs,ou,`compétence « ${q.skill} » au lieu de « ${k} »`,ex);
  if(q.level!==lv)note(out.erreurs,ou,`niveau ${q.level} au lieu de ${lv}`,ex);
  if(q.choices.length<2)note(out.erreurs,ou,'moins de 2 choix',ex);
  if(new Set(vs).size!==vs.length)note(out.erreurs,ou,'deux choix ont la même valeur',ex);
  // libellés comparés bruts : deux dessins différents donnent le même texte « [dessin] »
  const bruts=q.choices.map(c=>String(c.label).replace(/\s+/g,' ').trim());
  if(new Set(bruts).size!==bruts.length)note(out.erreurs,ou,'deux choix ont le même libellé',ex);
  const bons=vs.filter(v=>v===String(q.exp.c)).length;
  if(bons!==1)note(out.erreurs,ou,bons?'la bonne réponse est en double':"la bonne réponse n'est pas parmi les choix",ex+' → '+q.exp.c);
  const tout=[q.prompt,q.hint,q.explain].concat(q.choices.map(c=>c.label),q.choices.map(c=>c.why||'')).map(String).join(' ');
  const m=texte(tout).match(MOTS_INTERDITS);
  if(m)note(out.erreurs,ou,`« ${m[0]} » dans le texte`,ex);
  if(!texte(q.explain||''))note(out.erreurs,ou,'pas de correction (explain vide)',ex);
  if(!texte(q.hint||''))note(out.avertissements,ou,"pas d'indice (hint vide)",ex);
  q.choices.forEach(c=>{if(String(c.v)!==String(q.exp.c)&&!texte(c.why||''))note(out.avertissements,ou,'un mauvais choix sans « pourquoi »',ex+' → '+texte(c.label));});
  const bon=q.choices.find(c=>String(c.v)===String(q.exp.c));
  const liste=out.exemples[ou]||(out.exemples[ou]={});
  if(Object.keys(liste).length<PARAM.exemples)liste[texte(q.prompt)]=bon?texte(bon.label):'?';
}
function verifier(api){
  const {GEN,LEVELS,LEARN,SKILLS,EVAL_SKILLS}=api;
  if(!GEN||!LEVELS){note(out.erreurs,'page','window.__miniprofTirage doit recevoir au moins { GEN, LEVELS }');return;}
  const niveaux=Object.keys(LEVELS).map(Number);out.niveaux=niveaux;
  Object.keys(GEN).forEach(k=>{if(!PARAM.competences.includes(k))note(out.erreurs,'GEN',`« ${k} » n'est pas une compétence de la fiche`);});
  PARAM.competences.forEach(k=>{if(!GEN[k])note(out.avertissements,'fiche',`la compétence « ${k} » n'a pas de générateur`);});
  if(SKILLS)Object.keys(GEN).forEach(k=>{if(!SKILLS[k])note(out.erreurs,'SKILLS',`« ${k} » manque (libellé affiché)`);});
  (EVAL_SKILLS||[]).forEach(k=>{if(!GEN[k])note(out.erreurs,'EVAL_SKILLS',`« ${k} » n'a pas de générateur`);});
  for(const k of Object.keys(GEN))for(const lv of niveaux)for(let i=0;i<PARAM.tirages;i++){
    const ou=`${k}, niveau ${lv}`;out.tirages++;
    let q;try{q=GEN[k](lv);}catch(e){note(out.erreurs,ou,'le générateur plante : '+e.message);continue;}
    verifierQuestion(q,k,lv,ou);
  }
  (LEARN||[]).forEach((f,i)=>{
    const ou=`fiche Apprendre ${i+1}`;
    try{if(f.body)texte(f.body());}catch(e){note(out.erreurs,ou,"l'affichage plante : "+e.message);}
    if(!f.q)return;
    const vs=(f.q.c||[]).map(c=>String(c.v));
    if(vs.filter(v=>v===String(f.q.ok)).length!==1)note(out.erreurs,ou,'la petite question a 0 ou 2 bonnes réponses',texte(f.q.p));
    if(new Set(vs).size!==vs.length)note(out.erreurs,ou,'deux choix ont la même valeur',texte(f.q.p));
    (f.q.c||[]).forEach(c=>{if(String(c.v)!==String(f.q.ok)&&!texte(c.why||''))note(out.avertissements,ou,'un mauvais choix sans « pourquoi »',texte(f.q.p));});
  });
}
process.on('exit',()=>{
  if(!appele)note(out.erreurs,'page',"la page n'appelle pas window.__miniprofTirage (voir la fin de docs/gabarit-module.html)");
  process.stdout.write('\n@@TIRAGE@@'+JSON.stringify(out));
});
"""


def script_de_page(texte):
    """Les scripts classiques de la page (ni la fiche JSON, ni suivi.js), mis bout à bout."""
    return "\n".join(SCRIPT.findall(texte))


def tirer(path, tirages=2000, exemples=3):
    """Lance node sur la page ; renvoie (resultat, message d'échec). resultat est un dict ou None."""
    node = shutil.which("node")
    if not node:
        return None, "node introuvable : tirage impossible (installer node, ou le dire au parent)"
    texte = Path(path).read_text(encoding="utf-8")
    rapport = Rapport()
    fiche = lire_fiche(texte, rapport) or {}
    competences = [s.get("id") for s in fiche.get("skills", []) if isinstance(s, dict)]
    param = json.dumps({"tirages": tirages, "exemples": exemples, "competences": competences})
    code = HARNAIS.replace("__PARAM__", param) + "\n" + script_de_page(texte)
    with tempfile.TemporaryDirectory() as d:
        js = Path(d) / "tirage.js"
        js.write_text(code, encoding="utf-8")
        p = subprocess.run([node, str(js)], capture_output=True, text=True, timeout=600)
    if "@@TIRAGE@@" not in p.stdout:
        return None, "la page ne se charge pas dans node :\n" + (p.stderr.strip()[-1500:] or p.stdout[-1500:])
    resultat = json.loads(p.stdout.split("@@TIRAGE@@", 1)[1])
    if p.returncode != 0 and not resultat["erreurs"]:
        resultat["erreurs"]["page"] = {"n": 1, "ex": p.stderr.strip()[-800:]}
    return resultat, None


def afficher(path, r):
    print(f"{path} : {r['tirages']} questions tirées (niveaux {', '.join(map(str, r['niveaux']))})")
    for titre, table in (("Erreurs", r["erreurs"]), ("Avertissements", r["avertissements"])):
        if table:
            print(f"\n{titre} :")
            for msg, e in table.items():
                print(f"  ✘ {msg} ({e['n']} fois)" if titre == "Erreurs" else f"  ⚠ {msg} ({e['n']} fois)")
                if e["ex"]:
                    print(f"      ex. {e['ex'][:300]}")
    print("\nExemples à relire (question → bonne réponse) :")
    for ou, liste in r["exemples"].items():
        print(f"  {ou}")
        for q, rep in liste.items():
            print(f"    - {q[:200]} → {rep[:80]}")
    print()
    if r["erreurs"]:
        print(f"✘ {len(r['erreurs'])} sorte(s) d'erreur : corriger les générateurs, puis relancer.")
    else:
        print("✔ aucune erreur de forme. Relire les exemples : l'outil ne vérifie pas le fond.")


def main():
    parser = argparse.ArgumentParser(description="Tire des questions d'un module HTML et vérifie chacune.")
    parser.add_argument("fichiers", nargs="+", type=Path)
    parser.add_argument("--tirages", type=int, default=2000, help="questions par compétence et par niveau")
    parser.add_argument("--exemples", type=int, default=3, help="exemples affichés par compétence et niveau")
    args = parser.parse_args()
    code = 0
    for path in args.fichiers:
        r, echec = tirer(path, args.tirages, args.exemples)
        if echec:
            print(f"✘ {path} : {echec}")
            code = 2
            continue
        afficher(path, r)
        if r["erreurs"] and code == 0:
            code = 1
    sys.exit(code)


if __name__ == "__main__":
    main()
