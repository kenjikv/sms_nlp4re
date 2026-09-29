"""Valida integridad y denominadores; no constituye revisión semántica humana."""
from collections import Counter
from comun import ROOT, leer, guardar_json, lista
from recalcular_resultados import calcular, seleccion
import hashlib
def validar():
 checks=[]
 def ok(condition,label):
  assert condition,label
  checks.append(label)
 ext=leer(ROOT/'datos/extraccion/estudios_incluidos.csv');sel=leer(ROOT/'datos/seleccion/seleccion_global_cribado.csv')
 inv=leer(ROOT/'datos/recursos/inventario_RQ3_unidades_verificado.csv');pairs=leer(ROOT/'datos/recursos/rq3_pares_estudio_unidad.csv')
 ledger=leer(ROOT/'datos/seleccion/descubrimiento_arxiv_v8.csv');new=leer(ROOT/'datos/extraccion/incorporaciones_v8.csv')
 for rows,key,name in [(ext,'rid','extracción'),(sel,'rid','selección'),(inv,'unidad','inventario'),(ledger,'arxiv','descubrimiento')]:ok(len(rows)==len({x[key] for x in rows}),f'Identificadores únicos en {name}')
 ok({r['rid'] for r in ext}=={r['rid'] for r in sel if r['estado']=='INCLUIDO'},'Selección y extracción contienen los mismos incluidos')
 ok(len(ext)==550 and len(new)==11,'539 inclusiones conservadas y once incorporaciones')
 base=leer(ROOT/'datos/versiones_previas/estudios_incluidos_v7.csv');current={r['rid']:r for r in ext}
 ok(all(all(current[r['rid']][k]==v for k,v in r.items()) for r in base),'Todos los campos de los 539 estudios previos se conservan')
 ok(len({r['doi'].lower() for r in new})==11 and all(r['estado_publicacion'].startswith('publicación formal') for r in new),'Nuevos DOI únicos con publicación editorial confirmada')
 ok(len(ledger)==300 and sum(Counter(x['estado'] for x in ledger).values())==300,'Los 300 resultados de arXiv tienen estado de seguimiento')
 ok(sum(x['estado']=='INCLUIDO_V8' for x in ledger)==11,'Solo candidatos verificados pasan al corpus')
 ok(sum(x['estado']=='PENDIENTE_DE_CRIBADO' for x in ledger)==263,'263 registros sin cribar separados de los incluidos')
 ok({r['rid'] for r in leer(ROOT/'datos/seleccion/pendientes_texto_completo.csv')}=={r['rid'] for r in sel if r['estado']=='NO_EVALUABLE'},'267 pendientes históricos conservados')
 used=[p for p in pairs if p['cuenta_como_uso_rq3']=='True'];units={u['unidad']:u for u in inv}
 ok(len(used)==len({(p['rid'],p['unidad']) for p in used}),'Pares estudio–recurso contados una sola vez')
 ok(all(p['rid'] in current and p['unidad'] in units for p in used),'Usos enlazados a estudios y unidades existentes')
 ok(all(p['estado_rq3']==units[p['unidad']]['estado_rq3'] for p in used),'Inventario y usos comparten clasificación lingüística')
 ok(all(all(v['verificada'] for v in lista(r['recursos'])) for r in new),'Anclas de recursos nuevos localizadas en el texto')
 s=calcular();f=seleccion()
 for k in ['anio','tarea','tipo_evaluacion']:ok(sum(s[k].values())==544,f'Partición completa de {k} sobre 544 estudios')
 ok(sum(s['rq3_recursos'].values())==132 and len(used)==389,'132 recursos concretos y 389 usos')
 ok(len({p['rid'] for p in used})==204,'Recursos concretos en 204 estudios')
 ok(len(s['espanol'])==8,'Ocho estudios con datos españoles explícitos')
 ok(f['identificados']==f['cribados']+f['duplicados'] and f['cribados']==f['excluidos']+f['incluidos']+f['no_evaluados'],'Balance de selección canónica; descubrimiento parcial separado')
 archivo_textos=ROOT/'evidencia_local/textos_usados_verificacion.csv'
 omitidos=[]
 if archivo_textos.exists():
  texts={r['rid']:r['texto_usado'] for r in leer(archivo_textos)}
  for r in leer(ROOT/'datos/auditoria/incorporaciones_v8.csv'):ok(hashlib.sha256(texts[r['rid']].encode()).hexdigest()==r['sha256_texto'],'Integridad del texto '+r['rid'])
 else:
  omitidos=['Integridad del texto '+r['rid'] for r in leer(ROOT/'datos/auditoria/incorporaciones_v8.csv')]
 guardar_json(ROOT/'resultados/validacion.json',{'version':'v8','resultado':'correcto','comprobaciones':checks,'comprobaciones_locales_no_ejecutadas':omitidos,'alcance':'Integridad documental y computacional de esta actualización. Complementa la validación del autor en el corpus previo; no evalúa ni reemplaza la revisión humana de los nuevos registros.'})
 print(f'Validación v8 correcta: {len(checks)} comprobaciones; {len(omitidos)} controles de textos reservados al archivo local.')
if __name__=='__main__':validar()
