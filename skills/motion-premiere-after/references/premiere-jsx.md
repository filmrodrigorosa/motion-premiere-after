# ExtendScript pro Premiere (invoke_tool → execute_extendscript, arg `script`, sempre com `return`)

## Importar comps por Dynamic Link e pôr na V2
```js
var root=app.project.rootItem, bin=null;
for(var i=0;i<root.children.numItems;i++) if(root.children[i].name=='MOTION_AE') bin=root.children[i];
if(!bin) bin=root.createBin('MOTION_AE');
app.project.importAEComps('<caminho.aep>', ['MG_01_...','MG_03_...'], bin);
var plan={'MG_01':46,'MG_03':276}; // quadro de início (23,976)
var tr=app.project.activeSequence.videoTracks[1];
for(var j=0;j<bin.children.numItems;j++){var it=bin.children[j], k=it.name.substr(0,5);
  if(plan[k]!==undefined){var t=new Time(); t.seconds=plan[k]/23.976; tr.overwriteClip(it,t);}}
return 'ok';
```

## Zoom com ease assado quadro a quadro
```js
var tr=app.project.activeSequence.videoTracks[0], F=1/23.976;
var P=[0.652,0.587], C=[0.5,0.5]; // exemplo: pessoa à direita (normalizado); escala alvo ~140%
function mot(cl){for(var c=0;c<cl.components.numItems;c++) if(cl.components[c].matchName=='AE.ADBE Motion') return cl.components[c];}
function clipAt(s){for(var i=0;i<tr.clips.numItems;i++) if(Math.abs(tr.clips[i].start.seconds-s)<0.02) return tr.clips[i];}
function ease(x){return x<0.5?4*x*x*x:1-Math.pow(-2*x+2,3)/2;}
function lerp(a,b,e){return a.length?[a[0]+(b[0]-a[0])*e,a[1]+(b[1]-a[1])*e]:a+(b-a)*e;}
function bake(cl,prop,keys){ // keys: [[tempoTimeline, valor], ...]
  prop.setTimeVarying(false); prop.setTimeVarying(true);
  for(var k=0;k<keys.length;k++){var t0=keys[k][0],v0=keys[k][1];
    if(k+1<keys.length){var t1=keys[k+1][0],v1=keys[k+1][1];
      var same=v0.length?(v0[0]==v1[0]&&v0[1]==v1[1]):v0==v1;
      var n=same?1:Math.max(1,Math.round((t1-t0)/F));
      for(var s=0;s<n;s++){var tl=t0+(t1-t0)*s/n, tm=cl.inPoint.seconds+(tl-cl.start.seconds);
        prop.addKey(tm); prop.setValueAtKey(tm,lerp(v0,v1,ease(s/n)),true);}}
    else {var tm2=cl.inPoint.seconds+(t0-cl.start.seconds); prop.addKey(tm2); prop.setValueAtKey(tm2,v0,true);}}}
var cl=clipAt(1.919), m=mot(cl);
bake(cl,m.properties[1],[[1.919,100],[2.42,142]]);
bake(cl,m.properties[0],[[1.919,C],[2.42,P]]);
return 'ok';
```
- `setTimeVarying(false)` apaga os keys antigos do clipe. Se o clipe já tinha zoom, recrie os keys dele na mesma chamada.
- Um clipe que nasce de um corte herda os keys do original (ex.: fica em 112%). Refaça os keys dele também.

## Importar SFX
```js
var f=new Folder('<pasta de SFX>'), fs=f.getFiles('*.wav'), p=[];
for(var j=0;j<fs.length;j++) if(fs[j].name.charAt(0)!='.') p.push(fs[j].fsName);
app.project.importFiles(p,true,bin,false);
```
Depois: `audioTracks[1|2].overwriteClip(item, t)`, em ordem cronológica.
