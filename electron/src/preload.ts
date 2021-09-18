import { contextBridge } from 'electron';
import { execFile } from 'child_process';
import path from 'path';
import { promisify } from 'util';

const execFilePromise = promisify(execFile);

// eslint-disable-next-line @typescript-eslint/promise-function-async
export const runThoth = (
  filepath: string,
): ReturnType<typeof execFilePromise> => {
  const command = path.join(process.resourcesPath, 'thoth_engine');
  const args = ['--target', filepath];

  return execFilePromise(command, args);
};

export const getDirname = path.dirname;

contextBridge.exposeInMainWorld('thoth', {
  runThoth: runThoth,
  getDirname: getDirname,
});
