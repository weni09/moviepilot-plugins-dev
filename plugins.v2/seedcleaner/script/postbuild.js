// script/postbuild.js
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { globby } from 'globby';
import { rimraf } from 'rimraf';

const __dirname = dirname(fileURLToPath(import.meta.url));
const distDir = join(__dirname, '../dist');

// 要删除的文件匹配模式
const patterns = [
  'dist/assets/V*',
  'dist/assets/*.woff*',
  'dist/assets/*.ttf',
  'dist/assets/*.eot',
];

async function cleanUp() {
  const files = await globby(patterns, { dot: true });

  for (const file of files) {
    const fullPath = join(distDir, '..', file);
    try {
      await rimraf(fullPath);
      console.log(`已删除: ${file}`);
    } catch (err) {
      console.warn(`无法删除: ${file}`, err.message);
    }
  }

  // ✅ 可选：删除空目录本身
  // const dirToRemove = join(distDir, '../dist/assets/__federation_shared_vuetify');
  // try {
  //   await rimraf(dirToRemove);
  //   console.log(`已删除目录: ${dirToRemove}`);
  // } catch (err) {
  //   console.warn(`无法删除目录: ${dirToRemove}`, err.message);
  // }
}

cleanUp();