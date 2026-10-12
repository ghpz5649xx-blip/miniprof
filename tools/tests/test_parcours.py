"""Tests du parcours du module « Dictée 5 » (plan P012, pilote).

Pourquoi : la jauge, la série et le choix de l'étape suivante sont recalculés depuis le journal
de l'enfant à chaque écran. Une erreur de calcul fausserait ce qu'il voit (une étoile perdue,
une série remise à zéro à tort). On fait tourner les vraies fonctions de la page avec node, sans
navigateur, sur des historiques fabriqués.
"""

import json
import re
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
MODULE = ROOT / "modules" / "francais-cm1-dictee-5-avoir-etre.html"

# Même principe que tools/tirage.py : un faux document, puis la page donne ses fonctions.
HARNAIS = r"""
'use strict';
const bouchon=()=>new Proxy(function(){},{
  get:(t,k)=>k===Symbol.toPrimitive?(()=>''):(k==='innerHTML'||k==='textContent'?'':bouchon()),
  apply:()=>bouchon(),set:()=>true});
globalThis.document=bouchon();globalThis.location={};
let API=null;
globalThis.window={scrollTo(){},matchMedia:()=>({matches:false}),addEventListener(){},
  __miniprofTirage:api=>{API=api;}};
__PAGE__
const P=API.PARCOURS;
// Fabrique d'événements : t en secondes, q = "parcours/<skill>" sauf si libre.
const ev=(t,skill,juste,mode='e',niv=1,libre=false)=>({date:t,skill,juste,mode,difficulty:niv,
  question:libre?skill:'parcours/'+skill});
const R={};
__SCENARIOS__
process.stdout.write(JSON.stringify(R));
"""

SCENARIOS = r"""
// 1. Gains : Fibonacci de la série, plafonné à 8 ; l'étoile à 40 points.
{ const e=[];for(let i=0;i<10;i++)e.push(ev(1000+i*10,'noms',true));
  const pts=[];for(let i=1;i<=10;i++){const s=P.etatParcours(e.slice(0,i));pts.push(s.ouverte?s.ouverte.points:-1);}
  R.gains=pts;R.etoile=P.etatParcours(e).etoiles;R.fib=[1,2,3,4,5,6,7].map(P.gainSerie);
  R.apresEtoile=P.etatParcours(e).etapes.length; }
// 2. Deuxième chance réussie : la série est sauvée ; ratée : remise à zéro.
{ const base=[ev(1,'avoir',true),ev(2,'avoir',true),ev(3,'avoir',true),ev(4,'avoir',false)];
  R.sauvee=P.etatParcours(base.concat([ev(5,'avoir',true,'r')])).serie;
  R.perdue=P.etatParcours(base.concat([ev(5,'avoir',false,'r')])).serie;
  R.sansChance=P.etatParcours(base.concat([ev(6,'avoir',true)])).serie;
  R.pointsSauvee=P.etatParcours(base.concat([ev(5,'avoir',true,'r'),ev(6,'avoir',true)])).ouverte.points; }
// 3. Une pause de plus de 30 minutes remet la série à zéro, pas la jauge.
{ const e=[ev(0,'etre',true),ev(10,'etre',true),ev(20,'etre',true),ev(20+31*60,'etre',true)];
  const s=P.etatParcours(e);R.pause=[s.serie,s.ouverte.points];
  R.serieAffichee=P.serieActuelle(P.etatParcours(e.slice(0,3)),20+31*60); }
// 4. Les réponses hors parcours (entraînement libre, évaluation) ne remplissent pas la jauge.
{ const e=[ev(1,'noms',true,'e',1,true),ev(2,'noms',true,'v',1,true)];
  R.libre=P.etatParcours(e).etapes.length; }
// 5. Choix de l'étape : la compétence sans étoile la plus fragile d'abord.
{ const hist=[];
  for(let i=0;i<5;i++)hist.push(ev(i,'nature',false,'e',1,true));   // nature : 0 %
  for(let i=0;i<5;i++)hist.push(ev(10+i,'noms',true,'e',1,true));   // noms : 100 %
  const s=P.etatParcours(hist);
  R.premier=P.prochaineEtape(s,hist,100); }
// 6. Jamais deux fois la même compétence de suite ; puis révision quand tout a son étoile.
{ const skills=['noms','mots','nature','avoir','etre'];const h=[];let t=0;
  // une étape réussie sans faute jusqu'à son étoile
  const etoile=k=>{const n0=P.etatParcours(h).etoiles;while(P.etatParcours(h).etoiles===n0)h.push(ev(t+=5,k,true));};
  etoile('nature');
  R.apresNature=P.prochaineEtape(P.etatParcours(h),h,t).skill;
  skills.filter(k=>k!=='nature').forEach(k=>etoile(k));
  const s=P.etatParcours(h);R.toutes=s.etoiles;
  const unJourPlusTard=t+P.P.JOUR+1;
  R.revision=P.prochaineEtape(s,h,unJourPlusTard); }
// 7. Difficulté : +1 après 3 bonnes sur 4, -1 après 2 erreurs de suite.
{ R.monte=P.niveauApres(1,[true,false,true,true]).niv;
  R.descend=P.niveauApres(2,[true,false,false]).niv;
  R.reste=P.niveauApres(2,[true,false]).niv;
  R.plafond=P.niveauApres(3,[true,true,true]).niv;
  R.plancher=P.niveauApres(1,[false,false]).niv; }
// 8. Niveau de départ selon la maîtrise.
{ R.depart=[P.niveauDepart(null),P.niveauDepart(0.5),P.niveauDepart(0.7),P.niveauDepart(0.9)]; }
// 9. Une étape ouverte reste l'étape en cours, avec ses points (finie un autre jour).
{ const e=[ev(0,'mots',true),ev(5,'mots',true)];
  const p=P.prochaineEtape(P.etatParcours(e),e,5+3*P.P.JOUR);R.ouverte=[p.skill,p.points]; }
"""


@unittest.skipUnless(shutil.which("node"), "node introuvable")
class TestParcours(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        html = MODULE.read_text(encoding="utf-8")
        page = re.search(r"<script>(.*?)</script>", html, re.DOTALL).group(1)
        code = HARNAIS.replace("__PAGE__", page).replace("__SCENARIOS__", SCENARIOS)
        with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(code)
        sortie = subprocess.run(["node", f.name], capture_output=True, text=True, timeout=60)
        Path(f.name).unlink()
        if sortie.returncode != 0:
            raise AssertionError("node : " + sortie.stderr[-2000:])
        cls.r = json.loads(sortie.stdout)

    def test_gains_fibonacci_plafonne(self):
        self.assertEqual(self.r["fib"], [1, 1, 2, 3, 5, 8, 8])
        # 1, 2, 4, 7, 12, 20, 28, 36, puis 44 >= 40 : étoile (étape fermée)
        self.assertEqual(self.r["gains"][:8], [1, 2, 4, 7, 12, 20, 28, 36])
        self.assertEqual(self.r["gains"][8], -1)
        self.assertEqual(self.r["etoile"], 1)

    def test_deuxieme_chance(self):
        self.assertEqual(self.r["sauvee"], 3)
        self.assertEqual(self.r["perdue"], 0)
        self.assertEqual(self.r["sansChance"], 1, "une erreur sans deuxième chance perd la série")
        # 1 + 1 + 2 (série 3), erreur sauvée sans points, puis série 4 : +3
        self.assertEqual(self.r["pointsSauvee"], 7)

    def test_pause_remet_la_serie_a_zero(self):
        self.assertEqual(self.r["pause"], [1, 1 + 1 + 2 + 1])
        self.assertEqual(self.r["serieAffichee"], 0)

    def test_reponses_hors_parcours(self):
        self.assertEqual(self.r["libre"], 0)

    def test_choix_de_l_etape(self):
        self.assertEqual(self.r["premier"]["skill"], "nature")
        self.assertEqual(self.r["premier"]["niveau"], 1)
        self.assertFalse(self.r["premier"]["revision"])
        self.assertNotEqual(self.r["apresNature"], "nature")
        self.assertEqual(self.r["toutes"], 5)
        rev = self.r["revision"]
        self.assertTrue(rev["revision"])
        self.assertEqual(rev["skill"], "nature", "révision : l'étoile la plus ancienne")
        self.assertGreaterEqual(rev["niveau"], 2)

    def test_difficulte(self):
        self.assertEqual(self.r["monte"], 2)
        self.assertEqual(self.r["descend"], 1)
        self.assertEqual(self.r["reste"], 2)
        self.assertEqual(self.r["plafond"], 3)
        self.assertEqual(self.r["plancher"], 1)
        self.assertEqual(self.r["depart"], [1, 1, 2, 3])

    def test_etape_ouverte_gardee(self):
        self.assertEqual(self.r["ouverte"], ["mots", 2])


if __name__ == "__main__":
    unittest.main()
