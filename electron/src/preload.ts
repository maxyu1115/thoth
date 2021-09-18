import { contextBridge } from 'electron';
import { execFile } from 'child_process';
import path from 'path';
import { promisify } from 'util';

export const execFilePromise = promisify(execFile);

// eslint-disable-next-line @typescript-eslint/promise-function-async
const runThoth = (filepath: string): ReturnType<typeof execFilePromise> => {
  const command = path.join(process.resourcesPath, 'thoth_engine');
  const args = ['--target', filepath];

  return execFilePromise(command, args);
};

contextBridge.exposeInMainWorld('thoth', {
  runThoth: runThoth,
});
