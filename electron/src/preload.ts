import { contextBridge } from 'electron';
import { execFile } from 'child_process';
import path from 'path';
import { promisify } from 'util';

const execFilePromise = promisify(execFile);

// eslint-disable-next-line @typescript-eslint/promise-function-async
export const runThoth = (
  videoPath: string,
  outDir: string,
): ReturnType<typeof execFilePromise> => {
  const command = path.join(process.resourcesPath, 'thoth_engine');
  const args = ['--target', videoPath, '--output', outDir];

  return execFilePromise(command, args);
};

export const getDirname = path.dirname;

contextBridge.exposeInMainWorld('thoth', {
  runThoth: runThoth,
  getDirname: getDirname,
  joinPaths: path.join,
  getBasename: path.basename,
});
