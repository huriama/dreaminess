// Gera posts.json a partir de todos os artigos HTML na raiz do repositório.
const fs=require('node:fs');const path=require('node:path');
const files=fs.readdirSync('.').filter(f=>f.endsWith('.html')&&f!=='index.html'&&!f.startsWith('_'));
function match(s,re){const m=s.match(re);return m?m[1].trim():''}
function clean(s){return s.replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi,' ').replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi,' ').replace(/<[^>]+>/g,' ').replace(/&nbsp;/g,' ').replace(/&amp;/g,'&').replace(/&quot;/g,'"').replace(/&#39;/g,"'").replace(/\s+/g,' ').trim()}
const posts=files.map(file=>{
 const html=fs.readFileSync(file,'utf8');
 const title=clean(match(html,/<h1\b[^>]*>([\s\S]*?)<\/h1>/i)||match(html,/<title\b[^>]*>([\s\S]*?)<\/title>/i)||path.basename(file,'.html'));
 const description=match(html,/<meta\s+name=["']description["']\s+content=["']([^"']*)["']/i)||clean(match(html,/<(?:p)\b[^>]*>([\s\S]*?)<\/p>/i)).slice(0,220);
 const date=match(html,/<meta\s+name=["']post-date["']\s+content=["']([^"']*)["']/i);
 const image=match(html,/<meta\s+name=["']post-image["']\s+content=["']([^"']*)["']/i);
 const imageAlt=match(html,/<meta\s+name=["']post-image-alt["']\s+content=["']([^"']*)["']/i);
 return {url:encodeURI(file),title,description,date,image,imageAlt};
});
posts.sort((a,b)=>b.date.localeCompare(a.date)||b.url.localeCompare(a.url));
fs.writeFileSync('posts.json',JSON.stringify(posts,null,2)+'\n');
console.log(`Índice criado com ${posts.length} texto(s).`);
